"""生成20个典型画像冷启动案例"""
import json
from collections import Counter

cases = []

# ============ 保研赛道 5个 ============

# 1. 保研-本校
cases += [{
    "chunk_id": "2020级数科001号学长_profile_000", "type": "profile",
    "person_id": "2020级数科001号学长", "major": "数据科学与大数据技术", "stage": "2020级",
    "topic": "基础画像", "tags": ["画像","保研","本校"],
    "content": "姓名：2020级数科001号学长；年级：2020级；专业：数据科学与大数据技术；绩点3.9+；专业排名前5%；英语CET-6 520；核心竞赛：美赛M奖、全国大学生数学建模国一；科研成果：EI会议论文1篇（一作）；录取院校：本校保研。",
    "hometown_province": "", "gpa_band": "3.9+", "rank_band": "前5%", "data_source": "deep_interview", "completeness": "high"
},{
    "chunk_id": "2020级数科001号学长_timeline_001", "type": "timeline",
    "person_id": "2020级数科001号学长", "major": "数据科学与大数据技术", "stage": "2020级",
    "topic": "保研时间线", "tags": ["时间线","保研","本校"],
    "content": "大一上：高数线性代数打基础，绩点保持3.9。大一下：加入学院数据挖掘实验室。大二上：参加美赛拿M奖。大二暑假：数模国赛拿国一。大三上：完成EI论文投稿。大三下3月：准备夏令营材料。大三下6月：本校夏令营拿到offer。大四9月：预推免确认本校。",
    "data_source": "deep_interview"
},{
    "chunk_id": "2020级数科001号学长_advice_002", "type": "advice",
    "person_id": "2020级数科001号学长", "major": "数据科学与大数据技术", "stage": "2020级",
    "topic": "保研经验分享", "tags": ["建议","保研","本校"],
    "content": "本校保研的核心是绩点+科研双线并行。大一就进实验室不是越早越好，先打好数学和编程基础再进。科研产出要趁早，EI会议论文从投稿到录用周期6-8个月，大三上必须投出。本校导师联系最好在大三上学期，提前了解课题组方向。夏令营材料准备要针对性，个人陈述突出科研经历和成果。",
    "data_source": "deep_interview"
}]

# 2. 保研-外校顶尖(清华)
cases += [{
    "chunk_id": "2020级数科023号学长_profile_000", "type": "profile",
    "person_id": "2020级数科023号学长", "major": "数据科学与大数据技术", "stage": "2020级",
    "topic": "基础画像", "tags": ["画像","保研","清华"],
    "content": "姓名：2020级数科023号学长；年级：2020级；专业：数据科学与大数据技术；连续三年专业第一；绩点3.9+；英语CET-6 550；核心竞赛：美赛O奖、数模国赛国一、蓝桥杯国二；科研成果：SCI三区论文1篇；录取院校：清华大学。",
    "gpa_band": "3.9+", "rank_band": "专业第一", "data_source": "public_interview", "completeness": "high"
},{
    "chunk_id": "2020级数科023号学长_timeline_001", "type": "timeline",
    "person_id": "2020级数科023号学长", "major": "数据科学与大数据技术", "stage": "2020级",
    "topic": "保研清华时间线", "tags": ["时间线","保研","清华"],
    "content": "大一：绩点锁定专业第一，参加蓝桥杯拿国二。大二上：美赛备赛，最终拿O奖。大二暑假：数模国赛国一。大三上：SCI论文投稿，同时联系清华导师。大三下5月：清华夏令营报名。大三下7月：参加清华夏令营，面试表现突出拿到优营。大四9月：预推免正式录取清华。",
    "data_source": "public_interview"
},{
    "chunk_id": "2020级数科023号学长_advice_002", "type": "advice",
    "person_id": "2020级数科023号学长", "major": "数据科学与大数据技术", "stage": "2020级",
    "topic": "清华保研经验", "tags": ["建议","保研","清华"],
    "content": "绩点、竞赛、科研三头抓的关键是时间块管理法。每周日晚上规划下周时间，每天固定四个90分钟学习段，中间休息20分钟。清华夏令营看重科研潜力，面试时要把自己的论文讲清楚，包括动机、方法、创新点。个人陈述不要罗列奖项，要讲一条主线故事。避坑：海投夏令营不如精投3-5所针对性准备。",
    "data_source": "public_interview"
}]

# 3. 保研-外校顶尖(浙大)
cases += [{
    "chunk_id": "2021级数科038号学长_profile_000", "type": "profile",
    "person_id": "2021级数科038号学长", "major": "数据科学与大数据技术", "stage": "2021级",
    "topic": "基础画像", "tags": ["画像","保研","浙大"],
    "content": "姓名：2021级数科038号学长；年级：2021级；专业：数据科学与大数据技术；前两年绩点3.5-3.7；大三冲刺到3.7-3.8；专业排名前10%；英语CET-6 480；核心竞赛：数模国赛省一、蓝桥杯省一；科研成果：大创项目1项；录取院校：浙江大学。",
    "gpa_band": "3.7-3.8", "rank_band": "前10%", "data_source": "public_interview", "completeness": "high"
},{
    "chunk_id": "2021级数科038号学长_timeline_001", "type": "timeline",
    "person_id": "2021级数科038号学长", "major": "数据科学与大数据技术", "stage": "2021级",
    "topic": "大三冲刺保研时间线", "tags": ["时间线","保研","浙大"],
    "content": "大一至大二：绩点3.6左右徘徊，排名边缘。大三上：课程优先级管理，核心课重点突破，选修课合理搭配。大三上：主动联系导师进实验室。大三下3月：准备夏令营材料，打磨个人陈述。大三下6月：投递浙大夏令营。大三下7月：浙大夏令营面试通过拿优营。大四9月：预推免正式录取浙大。",
    "data_source": "public_interview"
},{
    "chunk_id": "2021级数科038号学长_advice_002", "type": "advice",
    "person_id": "2021级数科038号学长", "major": "数据科学与大数据技术", "stage": "2021级",
    "topic": "边缘保研经验", "tags": ["建议","保研","浙大"],
    "content": "绩点不高也能保研，关键是课程优先级管理。把核心课和高分课作为重点，选修课合理搭配保证不拖后腿。大三才开始冲刺完全来得及，但要系统规划。主动联系导师进实验室，即使从打杂开始也能积累科研经历。夏令营个人陈述要突出进步趋势而非绝对绩点。避坑：不要因为绩点不高就放弃保研，边缘人也有机会。",
    "data_source": "public_interview"
}]

# 4. 保研-外校顶尖(复旦跨方向)
cases += [{
    "chunk_id": "2021级智科021号学长_profile_000", "type": "profile",
    "person_id": "2021级智科021号学长", "major": "智能科学与技术", "stage": "2021级",
    "topic": "基础画像", "tags": ["画像","保研","复旦","跨方向"],
    "content": "姓名：2021级智科021号学长；年级：2021级；专业：智能科学与技术；绩点3.7-3.8；专业排名前10%；英语CET-6 510；核心竞赛：美赛H奖、互联网+省赛；科研成果：课程项目AI医学图像分割；录取院校：复旦大学工研院（跨方向申请生物医学工程）。",
    "gpa_band": "3.7-3.8", "rank_band": "前10%", "data_source": "public_interview", "completeness": "high"
},{
    "chunk_id": "2021级智科021号学长_advice_002", "type": "advice",
    "person_id": "2021级智科021号学长", "major": "智能科学与技术", "stage": "2021级",
    "topic": "跨方向保研经验", "tags": ["建议","保研","复旦","跨方向"],
    "content": "跨方向申请的关键是找到两个方向的结合点。我用AI方法做医学图像分割的课程项目，成为面试时最大亮点。准备阶段要研究目标院系导师方向，个人陈述强调跨学科优势。复旦工研院面试看重科研思路，会深挖项目细节。避坑：跨方向不是劣势，但必须证明你在交叉领域有实际产出，空谈兴趣没用。",
    "data_source": "public_interview"
}]

# 5. 保研-科研院所(中科院)
cases += [{
    "chunk_id": "2019级智科003号学长_profile_000", "type": "profile",
    "person_id": "2019级智科003号学长", "major": "智能科学与技术", "stage": "2019级",
    "topic": "基础画像", "tags": ["画像","保研","中科院"],
    "content": "姓名：2019级智科003号学长；年级：2019级；专业：智能科学与技术；绩点3.7-3.8；专业排名前10%；英语CET-6 500；核心竞赛：美赛M奖；科研成果：发明专利1项、软件著作权2项；录取院校：中科院信工所。",
    "gpa_band": "3.7-3.8", "rank_band": "前10%", "data_source": "deep_interview", "completeness": "high"
},{
    "chunk_id": "2019级智科003号学长_advice_002", "type": "advice",
    "person_id": "2019级智科003号学长", "major": "智能科学与技术", "stage": "2019级",
    "topic": "科研院所保研经验", "tags": ["建议","保研","中科院"],
    "content": "科研院所保研和高校不同，更看重工程能力和专利软著产出。专利软著比论文周期短，适合绩点不突出的同学快速产出。中科院信工所面试偏工程实操，会问具体技术实现细节。英语面试准备要提前，院所对英语有硬性要求。避坑：科研院所方向偏工程应用，想走纯学术路线的不太适合。",
    "data_source": "deep_interview"
}]

# ============ 考研赛道 4个 ============

# 6. 考研-本专业学硕
cases += [{
    "chunk_id": "2022级数科002号学长_profile_000", "type": "profile",
    "person_id": "2022级数科002号学长", "major": "数据科学与大数据技术", "stage": "2022级",
    "topic": "基础画像", "tags": ["画像","考研","学硕"],
    "content": "姓名：2022级数科002号学长；年级：2022级；专业：数据科学与大数据技术；绩点3.3-3.5；专业排名前30%；英语CET-4；考研方向：本专业学硕；录取院校：北京邮电大学计算机学院。",
    "gpa_band": "3.3-3.5", "rank_band": "前30%", "data_source": "deep_interview", "completeness": "high"
},{
    "chunk_id": "2022级数科002号学长_timeline_001", "type": "timeline",
    "person_id": "2022级数科002号学长", "major": "数据科学与大数据技术", "stage": "2022级",
    "topic": "考研备考时间表", "tags": ["时间线","考研","学硕"],
    "content": "大三上3月：确定考研，开始数学一轮。大三下4-6月：数学二轮+英语单词。大三暑假7-8月：专业课一轮（数据结构+操作系统），数学强化。大四上9-10月：政治开始，专业课二轮。大四上11-12月：全科冲刺，真题模拟。12月底：初试。次年3月：复试录取。",
    "data_source": "deep_interview"
},{
    "chunk_id": "2022级数科002号学长_advice_002", "type": "advice",
    "person_id": "2022级数科002号学长", "major": "数据科学与大数据技术", "stage": "2022级",
    "topic": "考研经验", "tags": ["建议","考研","学硕"],
    "content": "专业课复习误区：只看教材不做题是最大坑。数据结构必须手写代码，操作系统要画图理解。数学建议跟一个老师从头到尾，不要换。英语单词每天背不要断，阅读做真题就够。政治11月再开始不晚，跟肖四肖八。避坑：不要迷信经验帖的作息表，找到自己的节奏最重要。",
    "data_source": "deep_interview"
}]

# 7. 考研-本专业专硕
cases += [{
    "chunk_id": "2022级数科010号学长_profile_000", "type": "profile",
    "person_id": "2022级数科010号学长", "major": "数据科学与大数据技术", "stage": "2022级",
    "topic": "基础画像", "tags": ["画像","考研","专硕"],
    "content": "姓名：2022级数科010号学长；年级：2022级；专业：数据科学与大数据技术；绩点3.3-3.5；专业排名前30%；考研方向：本专业专硕；录取院校：北京理工大学计算机专硕。",
    "gpa_band": "3.3-3.5", "rank_band": "前30%", "data_source": "employment_cases", "completeness": "high"
},{
    "chunk_id": "2022级数科010号学长_advice_002", "type": "advice",
    "person_id": "2022级数科010号学长", "major": "数据科学与大数据技术", "stage": "2022级",
    "topic": "专硕考研经验", "tags": ["建议","考研","专硕"],
    "content": "专硕和学硕区别：专硕偏就业导向，学制2年，导师更放养。专硕分数线略低但竞争也不小。北理专硕专业课考408，难度和学硕一样。选专硕的原因是明确走就业路线，不想多花一年做科研。避坑：专硕不是水硕，该学的核心技术一样不能少，反而要更早准备实习。",
    "data_source": "employment_cases"
}]

# 8. 考研-跨考
cases += [{
    "chunk_id": "2022级智科015号学长_profile_000", "type": "profile",
    "person_id": "2022级智科015号学长", "major": "智能科学与技术", "stage": "2022级",
    "topic": "基础画像", "tags": ["画像","考研","跨考"],
    "content": "姓名：2022级智科015号学长；年级：2022级；专业：智能科学与技术；绩点3.0-3.3；专业排名前50%；考研方向：跨考金融科技；录取院校：中央财经大学金融科技方向。",
    "gpa_band": "3.0-3.3", "rank_band": "前50%", "data_source": "employment_cases", "completeness": "high"
},{
    "chunk_id": "2022级智科015号学长_advice_002", "type": "advice",
    "person_id": "2022级智科015号学长", "major": "智能科学与技术", "stage": "2022级",
    "topic": "跨考经验", "tags": ["建议","考研","跨考"],
    "content": "跨考最大的挑战是补基础。从智科跨金融科技，需要额外学微观经济学、金融学、计量经济学。建议大二下就开始旁听目标专业课程。跨考的优势是技术背景，金融科技方向很看重编程能力。避坑：跨考不要选跨度太大的方向，比如从工科跨法学几乎是从头开始。金融科技、计算法学这类交叉方向是甜点区。",
    "data_source": "employment_cases"
}]

# ============ 出国赛道 4个 ============

# 9. 出国-名校申请(NUS)
cases += [{
    "chunk_id": "2022级数科001号学长_profile_000", "type": "profile",
    "person_id": "2022级数科001号学长", "major": "数据科学与大数据技术", "stage": "2022级",
    "topic": "基础画像", "tags": ["画像","出国","名校","NUS"],
    "content": "姓名：2022级数科001号学长；年级：2022级；专业：数据科学与大数据技术；绩点3.7-3.8；专业排名前10%；英语：雅思7.5、GRE 325；核心竞赛：美赛M奖、Kaggle银牌；科研成果：1段海外暑研；录取院校：新加坡国立大学（NUS）计算机硕士。",
    "gpa_band": "3.7-3.8", "rank_band": "前10%", "data_source": "deep_interview", "completeness": "high"
},{
    "chunk_id": "2022级数科001号学长_timeline_001", "type": "timeline",
    "person_id": "2022级数科001号学长", "major": "数据科学与大数据技术", "stage": "2022级",
    "topic": "出国申请时间表", "tags": ["时间线","出国","NUS"],
    "content": "大二上：开始准备雅思，每天2小时。大二暑假：雅思考到7.5。大三上：准备GRE，12月考到325。大三寒假：联系海外教授套磁暑研。大三暑假：赴海外暑研3个月。大四上9-10月：选校定校，写文书。大四上11-12月：提交申请。大四下3月：收到NUS offer。",
    "data_source": "deep_interview"
},{
    "chunk_id": "2022级数科001号学长_advice_002", "type": "advice",
    "person_id": "2022级数科001号学长", "major": "数据科学与大数据技术", "stage": "2022级",
    "topic": "出国申请经验", "tags": ["建议","出国","NUS"],
    "content": "语言考试越早越好，大二就考完后面会轻松很多。GRE比雅思难，建议预留3-4个月。海外暑研是申请名校的关键加分项，大三寒假就要开始套磁。文书不要写流水账，要用故事线串联科研经历。选校要分梯度：冲刺校2所、匹配校3所、保底校2所。避坑：不要全投Top10，竞争激烈程度超出想象。",
    "data_source": "deep_interview"
}]

# 10. 出国-常规留学(爱丁堡)
cases += [{
    "chunk_id": "2021级智科012号学姐_profile_000", "type": "profile",
    "person_id": "2021级智科012号学姐", "major": "智能科学与技术", "stage": "2021级",
    "topic": "基础画像", "tags": ["画像","出国","常规留学","爱丁堡"],
    "content": "姓名：2021级智科012号学姐；年级：2021级；专业：智能科学与技术；绩点3.5-3.7；专业排名前20%；英语：雅思7.0；核心竞赛：美赛H奖；科研成果：课程项目2个；录取院校：英国爱丁堡大学AI硕士。",
    "gpa_band": "3.5-3.7", "rank_band": "前20%", "data_source": "public_interview", "completeness": "high"
},{
    "chunk_id": "2021级智科012号学姐_advice_002", "type": "advice",
    "person_id": "2021级智科012号学姐", "major": "智能科学与技术", "stage": "2021级",
    "topic": "常规留学经验", "tags": ["建议","出国","爱丁堡"],
    "content": "英国申请看重均分和院校背景，雅思可以后补。爱丁堡AI项目对双非友好，均分80+就有机会。文书重点写课程项目和实习经历，不需要科研论文。中介可以帮忙润色文书但选校要自己定。避坑：英国学校看专业排名而非综合排名，爱丁堡AI专业QS前10但综合排名不如G5。不要盲目冲G5，均分不够就是浪费时间。",
    "data_source": "public_interview"
}]

# ============ 就业赛道 7个 ============

# 11. 就业-大厂算法(华为CV)
cases += [{
    "chunk_id": "2020级智科014号学长_profile_000", "type": "profile",
    "person_id": "2020级智科014号学长", "major": "智能科学与技术", "stage": "2020级",
    "topic": "基础画像", "tags": ["画像","就业","算法","华为"],
    "content": "姓名：2020级智科014号学长；年级：2020级；专业：智能科学与技术；绩点3.5-3.7；专业排名前20%；英语CET-6；就业公司：华为成都研究所；就业岗位：算法工程师（CV方向）；工作城市：成都；薪资：应届20k-25k档；技术栈：Python、PyTorch、TensorFlow、OpenCV。",
    "hometown_province": "", "gpa_band": "3.5-3.7", "salary_band": "20k-25k", "target_company": "华为", "target_position": "算法工程师", "work_city": "成都", "data_source": "employment_cases", "completeness": "high"
},{
    "chunk_id": "2020级智科014号学长_timeline_001", "type": "timeline",
    "person_id": "2020级智科014号学长", "major": "智能科学与技术", "stage": "2020级",
    "topic": "算法岗实习路线", "tags": ["时间线","就业","算法","华为"],
    "content": "大二上：学完机器学习基础，跟着吴恩达课程。大二暑假：第一个小公司算法实习，做推荐系统。大三上：深度学习实战，打Kaggle比赛拿银牌。大三暑假：华为实习，做CV目标检测。大四上9月：秋招华为转正。面试常考：手撕CNN代码、目标检测YOLO原理、BN层推导、注意力机制。",
    "data_source": "employment_cases"
},{
    "chunk_id": "2020级智科014号学长_advice_002", "type": "advice",
    "person_id": "2020级智科014号学长", "major": "智能科学与技术", "stage": "2020级",
    "topic": "算法岗面经", "tags": ["建议","就业","算法","华为"],
    "content": "算法岗面试核心三块：ML基础、项目深度、手撕代码。ML基础必问逻辑回归推导、SVM、决策树、过拟合处理。项目要能说清数据流、模型选型、调参思路。手撕代码LeetCode中等难度够用。华为面试偏工程，会问部署和优化。避坑：不要只背八股文，面试官一追细节就露馅。至少做一个完整的端到端项目。",
    "data_source": "employment_cases"
}]

# 12. 就业-大厂算法(小米NLP)
cases += [{
    "chunk_id": "2021级智科009号学长_profile_000", "type": "profile",
    "person_id": "2021级智科009号学长", "major": "智能科学与技术", "stage": "2021级",
    "topic": "基础画像", "tags": ["画像","就业","算法","NLP","小米"],
    "content": "姓名：2021级智科009号学长；年级：2021级；专业：智能科学与技术；绩点3.3-3.5；专业排名前30%；英语CET-4；就业公司：小米武汉总部；就业岗位：AI算法工程师（NLP方向）；工作城市：武汉；薪资：应届20k-25k档；技术栈：Python、BERT、Transformer、PyTorch。",
    "gpa_band": "3.3-3.5", "salary_band": "20k-25k", "target_company": "小米", "target_position": "AI算法工程师", "work_city": "武汉", "data_source": "employment_cases", "completeness": "high"
},{
    "chunk_id": "2021级智科009号学长_advice_002", "type": "advice",
    "person_id": "2021级智科009号学长", "major": "智能科学与技术", "stage": "2021级",
    "topic": "NLP算法岗经验", "tags": ["建议","就业","算法","NLP","小米"],
    "content": "NLP岗现在必考大模型，BERT和Transformer原理是基础。小米面试会问预训练模型微调细节、prompt engineering。绩点不高也能进算法岗，关键是有NLP项目经历。建议大二就开始打Kaggle NLP比赛。避坑：不要只跑模型不看数据，数据处理占NLP工作70%。面试时数据清洗和特征工程的细节比模型选型更重要。",
    "data_source": "employment_cases"
}]

# 13. 就业-大厂工程开发(腾讯大数据)
cases += [{
    "chunk_id": "2020级数科012号学长_profile_000", "type": "profile",
    "person_id": "2020级数科012号学长", "major": "数据科学与大数据技术", "stage": "2020级",
    "topic": "基础画像", "tags": ["画像","就业","工程开发","腾讯"],
    "content": "姓名：2020级数科012号学长；年级：2020级；专业：数据科学与大数据技术；绩点3.5-3.7；专业排名前20%；英语CET-6；就业公司：腾讯深圳总部；就业岗位：大数据工程师；工作城市：深圳；薪资：应届15k-20k档，现30k以上档；技术栈：Scala、Spark、Kafka、Hive。",
    "gpa_band": "3.5-3.7", "salary_band": "15k-20k", "target_company": "腾讯", "target_position": "大数据工程师", "work_city": "深圳", "data_source": "employment_cases", "completeness": "high"
},{
    "chunk_id": "2020级数科012号学长_timeline_001", "type": "timeline",
    "person_id": "2020级数科012号学长", "major": "数据科学与大数据技术", "stage": "2020级",
    "topic": "大数据工程实习路线", "tags": ["时间线","就业","工程开发","腾讯"],
    "content": "大二上：学Hadoop生态，搭本地集群。大二暑假：小公司数据开发实习。大三上：深入Spark源码，写技术博客。大三暑假：腾讯实习，负责微信支付数据处理。大四上9月：秋招腾讯转正。面试常考：Spark RDD原理、Shuffle机制、Kafka消息可靠性、SQL优化、数据倾斜处理。",
    "data_source": "employment_cases"
},{
    "chunk_id": "2020级数科012号学长_advice_002", "type": "advice",
    "person_id": "2020级数科012号学长", "major": "数据科学与大数据技术", "stage": "2020级",
    "topic": "大数据工程面经", "tags": ["建议","就业","工程开发","腾讯"],
    "content": "大数据工程岗面试核心：SQL必考且难度高，会出窗口函数、行转列、连续登录等题。Spark原理要懂DAG、Stage划分、Shuffle。项目要能说清数据量和性能瓶颈。腾讯面试会追问系统设计。避坑：不要只会用API不懂原理，Spark面试必问源码级问题。建议读一遍Spark Core源码的核心模块。",
    "data_source": "employment_cases"
}]

# 14. 就业-大厂工程开发(拼多多)
cases += [{
    "chunk_id": "2021级数科013号学长_profile_000", "type": "profile",
    "person_id": "2021级数科013号学长", "major": "数据科学与大数据技术", "stage": "2021级",
    "topic": "基础画像", "tags": ["画像","就业","工程开发","拼多多"],
    "content": "姓名：2021级数科013号学长；年级：2021级；专业：数据科学与大数据技术；绩点3.3-3.5；专业排名前30%；英语CET-4；就业公司：拼多多上海总部；就业岗位：大数据开发工程师；工作城市：上海；薪资：应届20k-25k档，现25k-30k档；技术栈：Java、Hadoop、Spark、Flink。",
    "gpa_band": "3.3-3.5", "salary_band": "20k-25k", "target_company": "拼多多", "target_position": "大数据开发工程师", "work_city": "上海", "data_source": "employment_cases", "completeness": "high"
},{
    "chunk_id": "2021级数科013号学长_advice_002", "type": "advice",
    "person_id": "2021级数科013号学长", "major": "数据科学与大数据技术", "stage": "2021级",
    "topic": "拼多多面经", "tags": ["建议","就业","工程开发","拼多多"],
    "content": "拼多多面试偏Java后端，大数据岗也要会Java并发和JVM。Flink实时计算是拼多多重点考察方向。面试轮数多（4-5轮），每轮都有手撕代码。拼多多薪资高但工作强度大，11116是常态。避坑：不要只学大数据框架忽略Java基础，拼多多技术栈以Java为核心。Flink必学，拼多多实时数仓全用Flink。",
    "data_source": "employment_cases"
}]

# 15. 就业-央国企(华泰证券量化)
cases += [{
    "chunk_id": "2020级数科013号学长_profile_000", "type": "profile",
    "person_id": "2020级数科013号学长", "major": "数据科学与大数据技术", "stage": "2020级",
    "topic": "基础画像", "tags": ["画像","就业","央国企","金融","华泰证券"],
    "content": "姓名：2020级数科013号学长；年级：2020级；专业：数据科学与大数据技术；绩点3.5-3.7；专业排名前20%；英语CET-6；就业公司：华泰证券南京总部；就业岗位：量化分析师；工作城市：南京；薪资：应届15k-20k档，现25k-30k档；技术栈：Python、R、SQL、量化交易。",
    "gpa_band": "3.5-3.7", "salary_band": "15k-20k", "target_company": "华泰证券", "target_position": "量化分析师", "work_city": "南京", "data_source": "employment_cases", "completeness": "high"
},{
    "chunk_id": "2020级数科013号学长_advice_002", "type": "advice",
    "person_id": "2020级数科013号学长", "major": "数据科学与大数据技术", "stage": "2020级",
    "topic": "券商量化岗经验", "tags": ["建议","就业","央国企","金融","华泰证券"],
    "content": "券商量化岗面试分技术面和业务面。技术面考Python编程、SQL、统计学基础。业务面考金融市场知识、量化策略理解。华泰证券看重学校背景和专业匹配度。央国企优势是稳定、福利好，劣势是薪资涨幅不如互联网。避坑：量化岗不是纯技术岗，必须懂金融市场。建议考CFA一级或FRM增加竞争力。券商招聘看学历，研究生优势明显。",
    "data_source": "employment_cases"
}]

# 16. 就业-体制内(公务员)
cases += [{
    "chunk_id": "2021级智科016号学长_profile_000", "type": "profile",
    "person_id": "2021级智科016号学长", "major": "智能科学与技术", "stage": "2021级",
    "topic": "基础画像", "tags": ["画像","就业","体制内","公务员"],
    "content": "姓名：2021级智科016号学长；年级：2021级；专业：智能科学与技术；绩点3.3-3.5；专业排名前30%；英语CET-4；就业方向：体制内公务员；工作城市：省会城市；岗位：省大数据局技术岗。",
    "gpa_band": "3.3-3.5", "target_company": "省大数据局", "target_position": "技术岗公务员", "work_city": "省会城市", "data_source": "employment_cases", "completeness": "high"
},{
    "chunk_id": "2021级智科016号学长_advice_002", "type": "advice",
    "person_id": "2021级智科016号学长", "major": "智能科学与技术", "stage": "2021级",
    "topic": "体制内考公经验", "tags": ["建议","就业","体制内","公务员"],
    "content": "考公要趁应届身份，省考和国考岗位多。大数据局技术岗是近年新设岗位，竞争比普通岗小。笔试行测和申论是重点，技术知识面试才考。体制内优势是稳定、社会地位高，劣势是薪资低（到手8-12k）。备考周期建议3-6个月，行测靠刷题，申论靠积累。避坑：不要只盯国税海关这类热门岗，大数据局、网信办等技术岗性价比更高。",
    "data_source": "employment_cases"
}]

# 17. 就业-传媒数智化(AI产品经理)
cases += [{
    "chunk_id": "2021级智科010号学长_profile_000", "type": "profile",
    "person_id": "2021级智科010号学长", "major": "智能科学与技术", "stage": "2021级",
    "topic": "基础画像", "tags": ["画像","就业","传媒数智化","AI产品经理"],
    "content": "姓名：2021级智科010号学长；年级：2021级；专业：智能科学与技术；绩点3.5-3.7；专业排名前20%；英语CET-6；就业公司：微信广州总部；就业岗位：AI产品经理；工作城市：广州；薪资：应届25k-30k档，现30k以上档；技能：产品思维、AI技术理解、用户研究。",
    "gpa_band": "3.5-3.7", "salary_band": "25k-30k", "target_company": "微信", "target_position": "AI产品经理", "work_city": "广州", "data_source": "employment_cases", "completeness": "high"
},{
    "chunk_id": "2021级智科010号学长_advice_002", "type": "advice",
    "person_id": "2021级智科010号学长", "major": "智能科学与技术", "stage": "2021级",
    "topic": "AI产品经理经验", "tags": ["建议","就业","传媒数智化","AI产品经理"],
    "content": "AI产品经理是技术+产品的复合岗位，智科专业有天然优势。面试考三块：产品感觉（需求分析、竞品分析）、AI技术理解（模型能力边界、数据需求）、沟通能力。微信面试偏产品case分析，会问如何设计一个AI功能。建议大二开始做产品实习，积累PRD和原型设计经验。避坑：不要纯走技术路线，AI产品经理核心是产品思维而非代码能力。多写产品分析报告比刷题有用。",
    "data_source": "employment_cases"
}]

# 写入文件
output_path = 'edupilot_agent/data/cold_start_20.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)

# 统计
tracks = Counter()
people = set()
for c in cases:
    people.add(c['person_id'])
    for t in c.get('tags', []):
        if t in ('保研','考研','出国','就业'):
            tracks[t] += 1

print('生成完成: ' + str(len(cases)) + ' 条切片, ' + str(len(people)) + ' 人')
print('赛道分布:')
for t, n in tracks.most_common():
    print('  ' + t + ': ' + str(n) + ' 条切片')
print('文件: ' + output_path)
