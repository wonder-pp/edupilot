"""
Excel 底册 → JSON 切片 → FAISS 索引 转换脚本

将老师填写的 Excel 案例底册（一人一行）转换为系统使用的
JSON 切片格式（一人多条切片），并可直接触发 FAISS 索引重建。

字段对应：
  Excel 底册字段（23列）        →   切片字段
  ─────────────────────────────────────────────
  case_id                      →   chunk_id 前缀
  track                        →   type（保研/考研/出国/就业）
  graduation_year + major      →   person_id（脱敏代号）
  desensitized_id              →   person_id
  major                        →   major
  graduation_year              →   stage
  hometown_province            →   hometown_province
  gpa_band / rank_band / ...   →   content（拼成画像文本）
  timeline                     →   timeline 类型切片
  decisions                    →   decision 类型切片
  advice + pitfalls            →   advice 类型切片
  target_company/position/...  →   employment 类型切片

用法：
  # Excel → JSON（默认输出到 data/new_cases.json）
  python edupilot_agent/data/excel_to_json.py --input 老师填的底册.xlsx

  # Excel → JSON + 重建索引
  python edupilot_agent/data/excel_to_json.py --input 老师填的底册.xlsx --rebuild-index

  # 指定输出文件
  python edupilot_agent/data/excel_to_json.py --input 底册.xlsx --output data/custom.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List


def _split_semicolon(val: str) -> List[str]:
    """分号分隔的字符串 → 列表"""
    if not val or not val.strip():
        return []
    return [item.strip() for item in val.split(";") if item.strip()]


def _safe(val: Any) -> str:
    """安全转字符串，空值返回空串"""
    if val is None:
        return ""
    return str(val).strip()


def excel_row_to_records(row: Dict[str, Any]) -> List[dict]:
    """一行 Excel 底册数据 → 多条 JSON 切片记录
    每人生成 4 类切片：profile / timeline / advice / employment(或path)
    """
    # 基础字段
    case_id = _safe(row.get("案例编号 case_id"))
    track = _safe(row.get("赛道 track"))
    grad_year = _safe(row.get("毕业年份 graduation_year"))
    major = _safe(row.get("专业 major"))
    desens_id = _safe(row.get("脱敏代号 desensitized_id"))
    hometown = _safe(row.get("家乡省份 hometown_province"))
    gpa_band = _safe(row.get("GPA档次 gpa_band"))
    rank_band = _safe(row.get("排名档次 rank_band"))
    english = _safe(row.get("英语水平 english"))
    competitions = _split_semicolon(_safe(row.get("核心竞赛 core_competitions")))
    research = _split_semicolon(_safe(row.get("科研成果 research_outputs")))
    target_school = _safe(row.get("录取院校 target_school"))
    target_company = _safe(row.get("就业公司 target_company"))
    target_position = _safe(row.get("就业岗位 target_position"))
    work_city = _safe(row.get("工作城市 work_city"))
    salary_band = _safe(row.get("薪资区间 salary_band"))
    internships = _split_semicolon(_safe(row.get("关键实习 key_internships")))
    timeline_list = _split_semicolon(_safe(row.get("关键时间节点 timeline")))
    decisions = _split_semicolon(_safe(row.get("关键决策 decisions")))
    advice = _safe(row.get("经验建议 advice"))
    pitfalls = _safe(row.get("避坑建议 pitfalls"))
    data_source = _safe(row.get("数据来源 data_source")) or "manual_input"
    completeness = _safe(row.get("完整度 completeness")) or "medium"

    if not case_id or not desens_id:
        return []  # 空行跳过

    # stage 从毕业年份提取（"2024届" → "2024级"）
    stage = grad_year.replace("届", "级") if grad_year else ""

    records: List[dict] = []

    # === 切片1：profile（基础画像）===
    profile_parts = [f"姓名：{desens_id}"]
    if stage:
        profile_parts.append(f"年级：{stage}")
    if major:
        profile_parts.append(f"专业：{major}")
    if hometown:
        profile_parts.append(f"家乡：{hometown}")
    if gpa_band:
        profile_parts.append(f"绩点{gpa_band}")
    if rank_band:
        profile_parts.append(f"专业排名{rank_band}")
    if english:
        profile_parts.append(f"英语能力：{english}")
    if competitions:
        profile_parts.append(f"核心竞赛：{'、'.join(competitions)}")
    if research:
        profile_parts.append(f"科研成果：{'、'.join(research)}")

    # 赛道特定信息
    if track in ("保研", "考研", "出国") and target_school:
        profile_parts.append(f"录取院校：{target_school}")
    if track == "就业":
        if target_company:
            profile_parts.append(f"就业公司：{target_company}")
        if target_position:
            profile_parts.append(f"就业岗位：{target_position}")
        if work_city:
            profile_parts.append(f"工作城市：{work_city}")
        if salary_band:
            profile_parts.append(f"薪资：应届{salary_band}档")

    records.append({
        "chunk_id": f"{desens_id}_profile_000",
        "type": "profile",
        "person_id": desens_id,
        "major": major,
        "stage": stage,
        "topic": "基础画像",
        "content": "；".join(profile_parts) + "。",
        "tags": ["画像", "学业"] + ([track] if track else []),
        "hometown_province": hometown,
        "gpa_band": gpa_band,
        "rank_band": rank_band,
        "data_source": data_source,
        "completeness": completeness,
    })

    # === 切片2：timeline（关键时间节点）===
    if timeline_list:
        records.append({
            "chunk_id": f"{desens_id}_timeline_001",
            "type": "timeline",
            "person_id": desens_id,
            "major": major,
            "stage": stage,
            "topic": "关键时间节点",
            "content": "。".join(timeline_list) + "。",
            "tags": ["时间线", track] if track else ["时间线"],
            "data_source": data_source,
        })

    # === 切片3：advice（经验+避坑）===
    advice_parts = []
    if advice:
        advice_parts.append(advice)
    if pitfalls:
        advice_parts.append(f"避坑提醒：{pitfalls}")
    if advice_parts:
        records.append({
            "chunk_id": f"{desens_id}_advice_002",
            "type": "advice",
            "person_id": desens_id,
            "major": major,
            "stage": stage,
            "topic": "经验建议",
            "content": "。".join(advice_parts) + "。",
            "tags": ["建议", track] if track else ["建议"],
            "data_source": data_source,
        })

    # === 切片4：decisions（关键决策）===
    if decisions:
        records.append({
            "chunk_id": f"{desens_id}_decision_003",
            "type": "decision",
            "person_id": desens_id,
            "major": major,
            "stage": stage,
            "topic": "关键决策",
            "content": "。".join(decisions) + "。",
            "tags": ["决策", track] if track else ["决策"],
            "data_source": data_source,
        })

    # === 切片5：employment（就业赛道专用）===
    if track == "就业" and (target_company or target_position or internships):
        emp_parts = []
        if target_company:
            emp_parts.append(f"就业公司：{target_company}")
        if target_position:
            emp_parts.append(f"岗位：{target_position}")
        if work_city:
            emp_parts.append(f"城市：{work_city}")
        if salary_band:
            emp_parts.append(f"薪资：应届{salary_band}档")
        if internships:
            emp_parts.append(f"关键实习：{'；'.join(internships)}")

        records.append({
            "chunk_id": f"{desens_id}_employment_004",
            "type": "employment",
            "person_id": desens_id,
            "major": major,
            "stage": stage,
            "topic": f"就业案例-{target_company}{target_position}",
            "content": "。".join(emp_parts) + "。",
            "tags": ["就业", work_city, target_company, target_position],
            "target_company": target_company,
            "target_position": target_position,
            "work_city": work_city,
            "salary_band": salary_band,
            "hometown_province": hometown,
            "data_source": data_source,
        })

    # === 切片6：path（保研/考研/出国赛道专用）===
    if track in ("保研", "考研", "出国") and target_school:
        path_parts = [f"赛道：{track}", f"录取院校：{target_school}"]
        if competitions:
            path_parts.append(f"竞赛加分：{'、'.join(competitions)}")
        if research:
            path_parts.append(f"科研加分：{'、'.join(research)}")
        if english:
            path_parts.append(f"英语：{english}")

        records.append({
            "chunk_id": f"{desens_id}_path_004",
            "type": "path",
            "person_id": desens_id,
            "major": major,
            "stage": stage,
            "topic": f"{track}案例-{target_school}",
            "content": "。".join(path_parts) + "。",
            "tags": [track, target_school],
            "target_school": target_school,
            "data_source": data_source,
        })

    return records


def convert_excel_to_json(excel_path: str, output_path: str) -> int:
    """读取 Excel，转换为 JSON 切片，返回总切片数"""
    try:
        import openpyxl
    except ImportError:
        print("错误：需要 openpyxl 库，请运行 pip install openpyxl")
        return 0

    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb.active

    # 读取表头（第1行，格式"中文名\n英文key"）
    headers = []
    for cell in ws[1]:
        val = _safe(cell.value)
        if not val:
            break
        # 表头格式"案例编号\ncase_id" → "案例编号 case_id"
        parts = val.split("\n")
        if len(parts) >= 2:
            headers.append(f"{parts[0].strip()} {parts[1].strip()}")
        else:
            headers.append(val)
    print(f"读取到 {len(headers)} 列字段")

    # 逐行读取（第2行起，跳过标记为"示例行"的行）
    all_records: List[dict] = []
    row_count = 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        # 跳过空行
        if not row or not _safe(row[0]):
            continue
        # 跳过示例行（标记"←示例行"或"←xxx示例"）
        first_val = _safe(row[0])
        if first_val.startswith("←") or "示例" in first_val:
            continue

        # 组装行字典
        row_dict = {}
        for i, val in enumerate(row):
            if i >= len(headers):
                break
            row_dict[headers[i]] = val

        # 转换为切片
        records = excel_row_to_records(row_dict)
        if records:
            all_records.extend(records)
            row_count += 1
            print(f"  第{row_count}人: {row_dict.get('脱敏代号 desensitized_id', '')} → {len(records)} 条切片")

    # 写入 JSON
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_records, f, ensure_ascii=False, indent=2)

    print(f"\n转换完成：{row_count} 人 → {len(all_records)} 条切片")
    print(f"输出文件：{output_path}")
    return len(all_records)


def merge_to_existing(new_json_path: str, target_json: str = "edupilot_agent/data/employment_cases.json"):
    """将新生成的 JSON 合并到现有数据文件
    默认合并到 employment_cases.json（就业案例库）
    """
    # 读取新数据
    with open(new_json_path, "r", encoding="utf-8") as f:
        new_data = json.load(f)

    # 读取现有数据（如果存在）
    existing = []
    if os.path.exists(target_json):
        with open(target_json, "r", encoding="utf-8") as f:
            existing = json.load(f)

    # 合并（新数据追加到末尾）
    merged = existing + new_data

    # 写回
    with open(target_json, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"已合并到 {target_json}：现有 {len(existing)} 条 + 新增 {len(new_data)} 条 = {len(merged)} 条")


def main():
    parser = argparse.ArgumentParser(description="Excel 底册 → JSON 切片转换")
    parser.add_argument("--input", "-i", required=True,
                        help="Excel 底册文件路径")
    parser.add_argument("--output", "-o", default="edupilot_agent/data/new_cases.json",
                        help="输出 JSON 文件路径（默认 data/new_cases.json）")
    parser.add_argument("--merge", action="store_true",
                        help="合并到现有 employment_cases.json（不指定则只生成新文件）")
    parser.add_argument("--rebuild-index", action="store_true",
                        help="转换后自动重建 FAISS 索引")
    args = parser.parse_args()

    # 1. Excel → JSON
    print(f"[1/3] 读取 Excel: {args.input}")
    if not os.path.exists(args.input):
        print(f"错误：文件不存在 {args.input}")
        return

    count = convert_excel_to_json(args.input, args.output)
    if count == 0:
        print("未生成任何切片，请检查 Excel 内容")
        return

    # 2. 合并到现有数据（可选）
    if args.merge:
        print(f"\n[2/3] 合并到现有数据...")
        merge_to_existing(args.output)
    else:
        print(f"\n[2/3] 跳过合并（未指定 --merge）")

    # 3. 重建索引（可选）
    if args.rebuild_index:
        print(f"\n[3/3] 重建 FAISS 索引...")
        os.system(f"{sys.executable} edupilot_agent/langchain_index.py")
    else:
        print(f"\n[3/3] 跳过索引重建（未指定 --rebuild-index）")

    print("\n=== 完成 ===")
    if not args.merge:
        print(f"新数据在: {args.output}")
        print("如需合并到系统，运行：")
        print(f"  python {__file__} -i {args.input} --merge --rebuild-index")


if __name__ == "__main__":
    main()
