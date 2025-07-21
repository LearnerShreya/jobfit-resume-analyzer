"""
score_resume.py

Provides skill keyword dictionaries and a function to score resumes based on keyword matches for a given job role/domain. Now supports synonyms and partial matching.
"""
import re
from typing import Dict, List

# Domain-specific skill keywords for resume scoring
SKILL_KEYWORDS = {
    'Data Science': [
        'python', 'machine learning', 'data analysis', 'pandas', 'numpy',
        'regression', 'classification', 'deep learning', 'nlp',
        'tensorflow', 'keras', 'pytorch', 'sql', 'matplotlib',
        'scikit-learn', 'seaborn', 'bokeh', 'plotly', 'data visualization',
        'feature engineering', 'supervised learning', 'unsupervised learning',
        'statistics', 'data wrangling', 'data mining', 'predictive modeling',
        'big data', 'hadoop', 'spark', 'jupyter', 'notebook', 'data preprocessing'
    ],
    'Java Developer': [
        'java', 'spring', 'spring boot', 'hibernate', 'jpa', 'servlet', 'jsp', 'maven', 'gradle', 'junit',
        'rest api', 'microservices', 'tomcat', 'jboss', 'eclipse', 'intellij', 'oop', 'object oriented',
        'multithreading', 'concurrency', 'jdbc', 'sql', 'mysql', 'oracle', 'git', 'json', 'xml', 'lambda',
        'streams', 'collections', 'exception handling', 'design patterns', 'api development', 'unit testing',
        'jenkins', 'docker', 'kubernetes', 'aws', 'azure', 'cloud', 'ci/cd', 'log4j', 'swagger', 'mockito',
        'web services', 'soap', 'restful', 'jvm', 'garbage collection', 'performance tuning', 'debugging',
        'deployment', 'build automation', 'version control', 'agile', 'scrum', 'jira', 'uml', 'data structures',
        'algorithms'
    ],
    'Web Development': [
        'html', 'css', 'javascript', 'react', 'node.js', 'express', 'mongodb', 'frontend', 'backend', 'api',
        'rest', 'bootstrap', 'typescript', 'next.js', 'redux', 'vue', 'angular', 'sass', 'less', 'webpack',
        'babel', 'graphql', 'php', 'laravel', 'django', 'flask', 'mysql', 'sqlite', 'postgresql',
        'responsive design', 'ui', 'ux', 'websockets', 'jwt', 'oauth', 'authentication', 'authorization',
        'testing', 'jest', 'mocha', 'chai', 'cypress', 'storybook', 'material ui', 'tailwind', 'vercel',
        'netlify', 'heroku', 'aws', 'azure', 'cloud', 'api integration', 'restful', 'soap', 'web security',
        'seo', 'performance optimization', 'pwa', 'service worker', 'ssr', 'csr', 'spa', 'mvc', 'mvvm',
        'git', 'github', 'bitbucket', 'agile', 'scrum', 'jira'
    ],
    'Android Development': [
        'java', 'kotlin', 'android', 'xml', 'firebase', 'android studio', 'gradle', 'jetpack'
    ],
    'DevOps': [
        'docker', 'kubernetes', 'aws', 'azure', 'jenkins', 'ci/cd', 'terraform', 'ansible', 'monitoring'
    ],
    'Testing': [
        'selenium', 'junit', 'pytest', 'test case', 'testng', 'automation', 'manual testing'
    ],
    'Cloud Computing': [
        'aws', 'azure', 'gcp', 'cloud', 'lambda', 'ec2', 's3', 'devops'
    ],
    'Cyber Security': [
        'security', 'vulnerability', 'penetration testing', 'firewall', 'encryption', 'network security'
    ],
    'Networking': [
        'tcp/ip', 'dns', 'firewall', 'vpn', 'networking', 'routing', 'switching', 'protocols'
    ],
    'UI/UX': [
        'figma', 'wireframe', 'adobe xd', 'prototyping', 'ui', 'ux', 'design'
    ],
    'Business Analyst': [
        'requirement gathering', 'data analysis', 'process modeling', 'excel', 'dashboard', 'power bi',
        'tableau', 'communication', 'business process'
    ],
    'Software Development Engineer (SDE)': [
        'python', 'java', 'c++', 'c#', 'software engineering', 'object oriented', 'oop', 'data structures', 'algorithms',
        'system design', 'problem solving', 'git', 'github', 'unit testing', 'integration testing', 'sql', 'rest api',
        'microservices', 'cloud', 'aws', 'azure', 'docker', 'kubernetes', 'linux', 'agile', 'scrum', 'debugging',
        'version control', 'design patterns', 'code review', 'performance optimization', 'multithreading', 'concurrency'
    ],
    'Full Stack Developer': [
        'html', 'css', 'javascript', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring',
        'java', 'python', 'typescript', 'mongodb', 'mysql', 'postgresql', 'api', 'rest', 'graphql', 'redux', 'docker',
        'git', 'github', 'frontend', 'backend', 'responsive design', 'ui', 'ux', 'testing', 'agile', 'scrum', 'cloud',
        'aws', 'azure', 'devops', 'ci/cd', 'webpack', 'babel', 'sass', 'less', 'material ui', 'tailwind', 'heroku',
        'netlify', 'vercel', 'jwt', 'oauth', 'authentication', 'authorization', 'performance optimization'
    ]
}

# Synonyms for skill keywords (expand as needed)
SKILL_SYNONYMS: Dict[str, List[str]] = {
    'machine learning': ['ml'],
    'deep learning': ['dl'],
    'data analysis': ['data analytics', 'analytics'],
    'nlp': ['natural language processing'],
    'scikit-learn': ['sklearn'],
    'data wrangling': ['data cleaning'],
    'data mining': ['knowledge discovery'],
    'big data': ['large scale data'],
    'sql': ['structured query language'],
    'python': ['py'],
    'regression': ['linear regression', 'logistic regression'],
    'classification': ['binary classification', 'multi-class classification'],
    # Add more as needed
}

def _skill_in_text(skill: str, text: str) -> bool:
    """Return True if the skill or any synonym appears as a substring in the text."""
    skill = skill.lower()
    text = text.lower()
    if skill in text:
        return True
    for synonym in SKILL_SYNONYMS.get(skill, []):
        if synonym in text:
            return True
    return False

def calculate_score(resume_text: str, job_role: str) -> float:
    """
    Calculate the skill match score between resume content and required job role skills.
    Supports synonyms and partial (substring) matching.
    """
    if not resume_text or not job_role:
        return 0.0
    skills = SKILL_KEYWORDS.get(job_role.strip())
    if not skills:
        return 0.0
    resume_text = resume_text.lower().strip()
    matched_keywords = sum(
        1 for skill in skills if _skill_in_text(skill, resume_text)
    )
    total_keywords = len(skills)
    score = (matched_keywords / total_keywords) * 100 if total_keywords else 0.0
    return round(score, 2)