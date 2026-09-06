"""
EduPilot 数据脱敏与模糊化处理脚本

将 data/ 目录下的原始 JSON 切片处理为脱敏版，输出到 data/desensitized/。
处理规则（对应 DATA_SPEC.md 第三节）：
  1. person_id 真实姓名 → 脱敏代号（如 "2020级数科A学长"）
  2. content 文本中真实姓名 → 脱敏代号
  3. 精确薪资（"应届18K×15薪"）→ 区间档位（"15k-20k"）
  4. 精确 GPA（3.96）→ 档次（"3.9+"）
  5. 精确排名（1/65）→ 档次（"前5%"）
  6. 删除班级、导师姓名、微信号等私人联络信息

用法：
  python edupilot_agent/data/desensitize.py
  python edupilot_agent/data/desensitize.py --input edupilot_agent/data --output edupilot_agent/data/desensitized
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

# 专业 → 简称
MAJOR_SHORT = {
    "数据科学与大数据技术": "数科",
    "数据科学与大数据技术（传媒大数据方向）": "数科",
    "智能科学与技术": "智科",
}

# 薪资分档（左闭右开）
SALARY_BRACKETS: List[Tuple[str, int, int]] = [
    ("8k以下", 0, 8),
    ("8k-12k", 8, 12),
    ("12k-15k", 12, 15),
    ("15k-20k", 15, 20),
    ("20k-25k", 20, 25),
    ("25k-30k", 25, 30),
    ("30k以上", 30, 99999),
]


def fuzz_salary_value(k: int) -> str:
    """把应届月薪(K)映射到区间档位"""
    for label, lo, hi in SALARY_BRACKETS:
        if lo <= k < hi:
            return label
    return f"{k}k"


def fuzz_gpa_value(gpa: float) -> str:
    """精确 GPA → 档次"""
    if gpa >= 3.9:
        return "3.9+"
    if gpa >= 3.8:
        return "3.8-3.9"
    if gpa >= 3.7:
        return "3.7-3.8"
    if gpa >= 3.5:
        return "3.5-3.7"
    if gpa >= 3.0:
        return "3.0-3.5"
    return "3.0以下"


def fuzz_rank(rank: int, total: int) -> str:
    """精确排名 → 档次"""
    if total <= 0:
        return ""
    pct = rank / total
    if pct <= 0.05:
        return "前5%"
    if pct <= 0.10:
        return "前10%"
    if pct <= 0.20:
        return "前20%"
    if pct <= 0.30:
        return "前30%"
    return "前50%"


# 女性姓名特征字（用于判断学长/学姐）
_FEMALE_CHARS = set("丽娜婷莹颖敏静芳琳燕萍娟玲瑞瑶婉倩雯佳月颖")


def _guess_is_female(name: str) -> bool:
    """根据姓名特征字粗略判断性别，决定用"学长"还是"学姐" """
    if not name:
        return False
    for ch in name[-2:]:
        if ch in _FEMALE_CHARS:
            return True
    return False


def _normalize_stage(stage: str) -> str:
    """归一化届别：去空格、统一'级'字、过滤非届别值。
    '2020 级'/'2020级' → '2020级'
    '大一'/'大二' → 保留原值（非届别，但用于分组避免丢弃）"""
    s = stage.replace(" ", "").replace("\u3000", "")
    # 提取4位数字+级
    m = re.match(r"(\d{4})级?", s)
    if m:
        return m.group(1) + "级"
    return s  # 大一/大二/研一 等保留


def _normalize_major_short(major: str) -> str:
    """归一化专业简称：多个方向合并到主专业"""
    m = major.replace(" ", "").replace("\u3000", "")
    if "数科" in m or "数据科学" in m or "大数据" in m:
        return "数科"
    if "智科" in m or "智能科学" in m or "智能" in m:
        return "智科"
    if "光电" in m:
        return "光电"
    return "学生"


def build_name_mapping(records: List[dict]) -> Dict[str, str]:
    """构建全局 原始 person_id → 脱敏代号 映射。
    按 (归一化届别, 归一化专业简称) 分组，组内按出现顺序赋三位数字序号。
    序号格式 001/002/...，无 26 人上限。
    根据姓名特征字判断学长/学姐。"""
    mapping: Dict[str, str] = {}
    counters: Dict[Tuple[str, str], int] = {}

    for rec in records:
        pid = rec.get("person_id", "")
        if not pid:
            continue
        name_part = pid.split("_")[0].strip()
        if not name_part or name_part in mapping:
            continue
        if any(tag in name_part for tag in ("数科", "智科", "案例", "光电", "学生")):
            continue

        stage = _normalize_stage(rec.get("stage", ""))
        major_short = _normalize_major_short(rec.get("major", ""))
        key = (stage, major_short)
        idx = counters.get(key, 0)
        counters[key] = idx + 1
        tag = f"{idx + 1:03d}"  # 三位数字序号，容量无限
        suffix = "学姐" if _guess_is_female(name_part) else "学长"
        code = f"{stage}{major_short}{tag}号{suffix}"

        mapping[name_part] = code
        m = re.match(r"^([\u4e00-\u9fa5]{1,3}?)(学长|学姐|同学)$", name_part)
        if m:
            surname = m.group(1)
            for sfx in ("学长", "学姐", "同学"):
                variant = surname + sfx
                if variant not in mapping:
                    mapping[variant] = code

    return mapping


def desensitize_text(text: str, mapping: Dict[str, str]) -> str:
    """脱敏一段文本：替换姓名、模糊薪资、模糊GPA、删敏感信息"""
    if not text:
        return text
    result = text

    # 1. 替换真实姓名（按长度降序，避免短名误匹配）
    for real_name in sorted(mapping.keys(), key=len, reverse=True):
        short = real_name.split("_")[0].strip()
        code = mapping[real_name]
        if short and len(short) >= 2:
            result = result.replace(short, code)

    # 2. 薪资模糊化："应届18K×15薪" → "应届15k-20k档"
    def _salary_repl(m: re.Match) -> str:
        k = int(m.group(1))
        bracket = fuzz_salary_value(k)
        return f"应届{bracket}档"

    result = re.sub(r"应届(\d+)K[×x\*]\d+薪", _salary_repl, result)
    # "现25K×15薪" → "现20k-25k档"
    def _salary_now_repl(m: re.Match) -> str:
        k = int(m.group(1))
        bracket = fuzz_salary_value(k)
        return f"现{bracket}档"
    result = re.sub(r"现(\d+)K[×x\*]\d+薪", _salary_now_repl, result)

    # 3. GPA 模糊化：匹配 "绩点3.96"/"绩点：3.96"/"GPA为3.96"/"GPA3.96"
    def _gpa_repl(m: re.Match) -> str:
        try:
            gpa = float(m.group(1))
            return f"绩点{fuzz_gpa_value(gpa)}"
        except ValueError:
            return m.group(0)
    result = re.sub(r"(?:绩点|GPA)[为是：:]?\s*(\d+\.?\d*)", _gpa_repl, result)

    # 4. 精确排名模糊化："专业排名1/65"/"排名1/65"/"（专业排名1/65）"
    def _rank_repl(m: re.Match) -> str:
        try:
            r = int(m.group(1))
            t = int(m.group(2))
            band = fuzz_rank(r, t)
            return f"专业排名{band}" if band else m.group(0)
        except ValueError:
            return m.group(0)
    result = re.sub(r"(?:专业)?排名[：:]?\s*(\d+)/(\d+)", _rank_repl, result)

    # 5. 删除敏感联络信息：微信号、手机号、QQ群
    result = re.sub(r"(微信|微信号|wechat)[：:]?\s*[A-Za-z0-9_-]{5,}", "微信：已脱敏", result)
    result = re.sub(r"1[3-9]\d{9}", "[手机号已脱敏]", result)
    result = re.sub(r"QQ群[：:]?\s*\d{5,}", "QQ群：已脱敏", result)

    # 6. 删除导师真实姓名（"导师张某某" → "导师"）
    result = re.sub(r"导师[：:]?\s*[\u4e00-\u9fa5]{2,3}", "导师", result)

    # 7. 删除具体班级信息（"数科1班"/"智科2班"/"大数据3班" → "[班级已脱敏]"）
    result = re.sub(r"(数科|智科|大数据|数据科学|智能科学)[\u4e00-\u9fa5]{0,4}\d+班", "[班级已脱敏]", result)
    result = re.sub(r"\d+班", "[班级已脱敏]", result)

    return result


def desensitize_record(rec: dict, mapping: Dict[str, str]) -> dict:
    """脱敏单条记录"""
    out = dict(rec)
    # person_id
    pid = out.get("person_id", "")
    if pid in mapping:
        out["person_id"] = mapping[pid]
    elif pid and "_" in pid:
        name_part = pid.split("_")[0]
        if name_part in mapping:
            city = pid.rsplit("_", 1)[-1]
            out["person_id"] = f"{mapping[name_part]}_{city}"

    # chunk_id：替换前缀真实姓名为脱敏代号
    # 格式如 "王思远_profile_000" → "2020级数科A学长_profile_000"
    chunk_id = out.get("chunk_id", "")
    if isinstance(chunk_id, str) and "_" in chunk_id:
        parts = chunk_id.split("_", 1)
        name_prefix = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        if name_prefix in mapping:
            out["chunk_id"] = f"{mapping[name_prefix]}_{rest}"
        elif name_prefix in mapping.values():
            # 已是脱敏代号，保持不变
            pass
        else:
            # 尝试用 person_id 的脱敏结果替换
            desens_pid = out.get("person_id", "")
            if desens_pid and desens_pid != pid:
                out["chunk_id"] = f"{desens_pid}_{rest}"

    # gpa 字段精确值 → 档次
    gpa = out.get("gpa")
    if isinstance(gpa, (int, float)):
        out["gpa_band"] = fuzz_gpa_value(float(gpa))
        out["gpa"] = None

    # gpa_rank 字符串如 "1/68" → 档次
    gpa_rank_str = out.get("gpa_rank")
    if isinstance(gpa_rank_str, str) and "/" in gpa_rank_str:
        try:
            parts = gpa_rank_str.split("/")
            r, t = int(parts[0]), int(parts[1])
            out["gpa_rank"] = fuzz_rank(r, t)
            out["rank_band"] = out["gpa_rank"]
        except (ValueError, IndexError):
            pass
    elif isinstance(gpa_rank_str, (int, float)):
        total = out.get("total_students")
        if isinstance(total, (int, float)):
            out["rank_band"] = fuzz_rank(int(gpa_rank_str), int(total))
            out["gpa_rank"] = out["rank_band"]

    # content 文本脱敏
    content = out.get("content", "")
    if isinstance(content, str):
        out["content"] = desensitize_text(content, mapping)

    # topic 文本脱敏
    topic = out.get("topic", "")
    if isinstance(topic, str):
        out["topic"] = desensitize_text(topic, mapping)

    return out


# 大区映射（用于反向定位防护）
_PROVINCE_TO_REGION = {
    "河北": "华北", "山西": "华北", "内蒙古": "华北", "北京": "华北", "天津": "华北",
    "辽宁": "东北", "吉林": "东北", "黑龙江": "东北",
    "上海": "华东", "江苏": "华东", "浙江": "华东", "安徽": "华东", "福建": "华东",
    "江西": "华东", "山东": "华东", "台湾": "华东",
    "河南": "华中", "湖北": "华中", "湖南": "华中",
    "广东": "华南", "广西": "华南", "海南": "华南", "香港": "华南", "澳门": "华南",
    "重庆": "西南", "四川": "西南", "贵州": "西南", "云南": "西南", "西藏": "西南",
    "陕西": "西北", "甘肃": "西北", "青海": "西北", "宁夏": "西北", "新疆": "西北",
}

# 冷门公司关键词（小众公司更容易被反向定位）
_NICHE_COMPANY_KEYWORDS = ["红书", "得物", "B站", "哔哩", "米哈游", "莉莉丝", "叠纸",
                           "鹰角", "完美世界", "搜狐", "360", "搜狗", "知乎"]


def _apply_reverse_location_protection(records: List[dict]) -> List[dict]:
    """反向定位防护：当 hometown + 冷门公司 + 岗位三者组合可能定位个人时，
    将家乡省份退化为大区。"""
    from collections import Counter

    # 统计每个 (company, position) 组合出现次数
    combo_counter: Counter = Counter()
    for rec in records:
        company = rec.get("target_company", "") or ""
        pos = rec.get("target_position", "") or ""
        if company and pos:
            combo_counter[(company, pos)] += 1

    for rec in records:
        hometown = rec.get("hometown_province", "") or ""
        company = rec.get("target_company", "") or ""
        pos = rec.get("target_position", "") or ""

        if not hometown or not company:
            continue

        # 条件1：冷门公司（含关键词）+ 有岗位 + 有家乡
        is_niche = any(kw in company for kw in _NICHE_COMPANY_KEYWORDS)
        # 条件2：(公司+岗位)组合出现次数<=2（小样本易定位）
        combo_count = combo_counter.get((company, pos), 0)
        # 条件3：家乡已是精确省份（非大区）
        is_province = hometown.endswith("省") or hometown.endswith("市") or \
                      hometown in ("河北", "山西", "辽宁", "吉林", "黑龙江",
                                   "江苏", "浙江", "安徽", "福建", "江西", "山东",
                                   "河南", "湖北", "湖南", "广东", "广西", "海南",
                                   "重庆", "四川", "贵州", "云南", "陕西", "甘肃",
                                   "青海", "宁夏", "新疆")

        if is_niche and is_province and combo_count <= 2:
            # 退化到大区
            region = _PROVINCE_TO_REGION.get(hometown.replace("省", "").replace("市", ""), "")
            if region:
                rec["hometown_province"] = region + "地区"
                rec["_hometown_degraded"] = True  # 标记已退化

    return records


def process_file(input_path: Path, output_path: Path, mapping: Dict[str, str]) -> int:
    """处理单个 JSON 文件，返回处理条数"""
    with open(input_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    if not isinstance(records, list):
        print(f"  跳过 {input_path.name}（非数组结构）")
        return 0

    desensitized = [desensitize_record(rec, mapping) for rec in records]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(desensitized, f, ensure_ascii=False, indent=2)

    return len(desensitized)


def collect_all_records(data_dir: Path) -> List[dict]:
    """汇总所有 JSON 的记录，用于构建全局姓名映射"""
    all_records: List[dict] = []
    for json_file in data_dir.glob("*.json"):
        if json_file.name in ("case_template.json",):
            continue
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                records = json.load(f)
            if isinstance(records, list):
                all_records.extend(records)
        except (json.JSONDecodeError, OSError):
            continue
    return all_records


def main():
    parser = argparse.ArgumentParser(description="EduPilot 数据脱敏处理")
    parser.add_argument("--input", default="edupilot_agent/data",
                        help="原始数据目录")
    parser.add_argument("--output", default="edupilot_agent/data/desensitized",
                        help="脱敏输出目录")
    args = parser.parse_args()

    data_dir = Path(args.input)
    out_dir = Path(args.output)

    if not data_dir.exists():
        print(f"错误：输入目录不存在 {data_dir}")
        return

    # 1. 汇总所有记录，构建全局姓名映射
    print("[1/3] 扫描原始数据，构建姓名映射...")
    all_records = collect_all_records(data_dir)
    mapping = build_name_mapping(all_records)
    print(f"  共识别 {len(mapping)} 个真实姓名待脱敏")
    for real, code in list(mapping.items())[:10]:
        print(f"    {real} → {code}")
    if len(mapping) > 10:
        print(f"    ... 及其余 {len(mapping) - 10} 个")

    # 2. 逐文件处理
    print(f"\n[2/4] 处理 JSON 文件，输出到 {out_dir} ...")
    json_files = [f for f in data_dir.glob("*.json")
                  if f.name not in ("case_template.json",)]
    total = 0
    for json_file in sorted(json_files):
        out_file = out_dir / json_file.name
        n = process_file(json_file, out_file, mapping)
        print(f"  {json_file.name}: {n} 条 → {out_file.name}")
        total += n

    # 3. 反向定位防护：对脱敏后的全局数据跑一遍
    print(f"\n[3/4] 反向定位防护（冷门公司+岗位+籍贯组合检查）...")
    all_desensitized = collect_all_records(out_dir)
    degraded_count = sum(1 for r in all_desensitized if r.get("_hometown_degraded"))
    all_desensitized = _apply_reverse_location_protection(all_desensitized)
    # 重新写回 desensitized 目录（合并所有记录到统一文件）
    protection_path = out_dir / "_reverse_protection_applied.json"
    with open(protection_path, "w", encoding="utf-8") as f:
        json.dump(all_desensitized, f, ensure_ascii=False, indent=2)
    # 统计退化数量
    degraded_count = sum(1 for r in all_desensitized if r.get("_hometown_degraded"))
    print(f"  共 {degraded_count} 条记录的家乡省份已退化为大区")

    # 4. 导出姓名映射表（供审查）
    mapping_path = out_dir / "_name_mapping.json"
    with open(mapping_path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"\n[4/4] 姓名映射表已导出：{mapping_path}")
    print(f"\n完成：共处理 {total} 条记录，{len(mapping)} 个姓名已脱敏，{degraded_count} 条家乡退化。")
    print(f"脱敏版数据位于：{out_dir}")
    print("审查无误后，替换原文件并重建 FAISS 索引：")
    print(f"  python edupilot_agent/langchain_index.py")


if __name__ == "__main__":
    main()
