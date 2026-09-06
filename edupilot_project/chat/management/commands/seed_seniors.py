# -*- coding: utf-8 -*-
"""冷启动学长就业样本数据：17人脱敏案例，与FAISS冷启动数据保持一致。

数据来源：edupilot_agent/data/cold_start_20.json
脱敏规则：姓名=脱敏代号，薪资=区间档位，与DATA_SPEC.md一致

运行方式：
  python manage.py seed_seniors            # 增量写入（跳过已存在）
  python manage.py seed_seniors --flush    # 清空旧数据后重新写入（冷启动切换用）
"""
from django.core.management.base import BaseCommand, BaseCommand
from chat.models import SeniorMentor, SeniorEmployment

MAJOR_DS = '数据科学与大数据技术'
MAJOR_AI = '智能科学与技术'

# 级别→毕业年份映射（本科4年制）
STAGE_TO_YEAR = {
    '2019级': '2023',
    '2020级': '2024',
    '2021级': '2025',
    '2022级': '2026',
}

# 冷启动17人数据
# (脱敏代号, 专业, 级别, 就业类型, 单位, 行业, 岗位, 薪资区间, 工作地)
# 就业类型：fulltime=全职 / graduate=升学(保研+考研) / study_abroad=出国
SENIORS = [
    # ========== 保研赛道 5人 ==========
    ('2020级数科001号学长', MAJOR_DS, '2020级', 'graduate', '本校', '科研', '保研（本校）', '', '北京'),
    ('2020级数科023号学长', MAJOR_DS, '2020级', 'graduate', '清华大学', '科研', '保研（清华）', '', '北京'),
    ('2021级数科038号学长', MAJOR_DS, '2021级', 'graduate', '浙江大学', '科研', '保研（浙大）', '', '杭州'),
    ('2021级智科021号学长', MAJOR_AI, '2021级', 'graduate', '复旦大学', '科研', '保研（复旦跨方向）', '', '上海'),
    ('2019级智科003号学长', MAJOR_AI, '2019级', 'graduate', '中科院信工所', '科研', '保研（科研院所）', '', '北京'),

    # ========== 考研赛道 3人 ==========
    ('2022级数科002号学长', MAJOR_DS, '2022级', 'graduate', '北京邮电大学', '科研', '考研（学硕）', '', '北京'),
    ('2022级数科010号学长', MAJOR_DS, '2022级', 'graduate', '北京理工大学', '科研', '考研（专硕）', '', '北京'),
    ('2022级智科015号学长', MAJOR_AI, '2022级', 'graduate', '中央财经大学', '科研', '跨考（金融科技）', '', '北京'),

    # ========== 出国赛道 2人 ==========
    ('2022级数科001号学长', MAJOR_DS, '2022级', 'study_abroad', '新加坡国立大学', '科研', '名校申请（NUS）', '', '新加坡'),
    ('2021级智科012号学姐', MAJOR_AI, '2021级', 'study_abroad', '英国爱丁堡大学', '科研', '常规留学（AI硕士）', '', '英国'),

    # ========== 就业赛道 7人 ==========
    ('2020级智科014号学长', MAJOR_AI, '2020级', 'fulltime', '华为', '人工智能', '算法工程师（CV方向）', '20k-25k', '成都'),
    ('2021级智科009号学长', MAJOR_AI, '2021级', 'fulltime', '小米', '人工智能', 'AI算法工程师（NLP方向）', '20k-25k', '武汉'),
    ('2020级数科012号学长', MAJOR_DS, '2020级', 'fulltime', '腾讯', '互联网', '大数据工程师', '15k-20k', '深圳'),
    ('2021级数科013号学长', MAJOR_DS, '2021级', 'fulltime', '拼多多', '互联网', '大数据开发工程师', '20k-25k', '上海'),
    ('2020级数科013号学长', MAJOR_DS, '2020级', 'fulltime', '华泰证券', '金融科技', '量化分析师', '15k-20k', '南京'),
    ('2021级智科016号学长', MAJOR_AI, '2021级', 'fulltime', '省大数据局', '体制内', '技术岗公务员', '8k-12k', '省会城市'),
    ('2021级智科010号学长', MAJOR_AI, '2021级', 'fulltime', '微信', '互联网', 'AI产品经理', '25k-30k', '广州'),
]


def _build_education(major, year, company):
    return f'{year}届{major}本科，于{company}就职/深造'


def _build_summary(major, year, company, position, salary):
    if salary:
        return f'{year}年毕业后加入{company}担任{position}，薪资区间{salary}，工作中持续深耕{major}相关技术。'
    return f'{year}年毕业后进入{company}攻读{position}，继续{major}方向的研究。'


def _build_skills(major, etype):
    if etype == 'fulltime':
        return 'Python,SQL,机器学习,数据建模,大数据开发'
    if etype in ('graduate', 'study_abroad'):
        return '科研论文,算法基础,数学建模,Python'
    return '通用技能'


def _build_advice(major):
    return f'建议学弟学妹在校期间扎实{major}基础，多参加项目实战和竞赛，绩点和排名是保研/求职的关键。'


class Command(BaseCommand):
    help = '冷启动学长就业样本数据（17人脱敏案例，与FAISS冷启动数据一致）'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='清空旧数据后重新写入（冷启动切换用）',
        )

    def handle(self, *args, **options):
        if options.get('flush'):
            deleted_emp, _ = SeniorEmployment.objects.all().delete()
            deleted_mentor, _ = SeniorMentor.objects.all().delete()
            self.stdout.write(self.style.WARNING(
                f'已清空旧数据：删除 {deleted_mentor} 条学长档案，{deleted_emp} 条就业去向。'
            ))

        created = 0
        skipped = 0
        for (name, major, stage, etype, company, industry, position, salary, loc) in SENIORS:
            year = STAGE_TO_YEAR.get(stage, stage[:4])
            mentor, was_created = SeniorMentor.objects.get_or_create(
                name=name,
                defaults={
                    'major': major,
                    'graduation_year': year,
                    'current_status': f'就职于{company}' if etype == 'fulltime' else f'就读于{company}',
                    'company': company if etype == 'fulltime' else '',
                    'position': position,
                    'education_background': _build_education(major, year, company),
                    'experience_summary': _build_summary(major, year, company, position, salary),
                    'skills': _build_skills(major, etype),
                    'achievements': '',
                    'advice': _build_advice(major),
                    'mentor_type': 'career' if etype == 'fulltime' else 'academic',
                    'tags': f'{major},{year}届,{company}',
                },
            )
            if not was_created:
                skipped += 1
                continue
            SeniorEmployment.objects.create(
                senior=mentor,
                employment_type=etype,
                company_name=company,
                industry=industry,
                position=position,
                salary_range=salary,
                location=loc,
                work_summary=_build_summary(major, year, company, position, salary),
                recruitment_tips=_build_advice(major),
            )
            created += 1

        total_mentors = SeniorMentor.objects.count()
        total_emp = SeniorEmployment.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'完成：新增 {created} 位学长，跳过(已存在) {skipped} 位。'
            f'当前库内：学长档案 {total_mentors} 条，就业去向 {total_emp} 条。'
        ))
