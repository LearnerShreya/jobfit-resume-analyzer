import re

# Dictionary of domain-specific skill keywords
SKILL_KEYWORDS = {
    'Data Science': [
        'python', 'machine learning', 'data analysis', 'pandas', 'numpy',
        'regression', 'classification', 'deep learning', 'nlp',
        'tensorflow', 'keras', 'pytorch', 'sql', 'matplotlib',
        'scikit-learn', 'seaborn', 'bokeh', 'plotly', 'data visualization', 'feature engineering', 'supervised learning', 'unsupervised learning', 'statistics', 'data wrangling', 'data mining', 'predictive modeling', 'big data', 'hadoop', 'spark', 'jupyter', 'notebook', 'matplotlib', 'data preprocessing'
    ],
    'Java Developer': [
        'java', 'spring', 'spring boot', 'hibernate', 'jpa', 'servlet', 'jsp', 'maven', 'gradle', 'junit', 'rest api', 'microservices', 'tomcat', 'jboss', 'eclipse', 'intellij', 'oop', 'object oriented', 'multithreading', 'concurrency', 'jdbc', 'sql', 'mysql', 'oracle', 'git', 'json', 'xml', 'lambda', 'streams', 'collections', 'exception handling', 'design patterns', 'api development', 'unit testing', 'jenkins', 'docker', 'kubernetes', 'aws', 'azure', 'cloud', 'ci/cd', 'log4j', 'swagger', 'mockito', 'web services', 'soap', 'restful', 'jvm', 'garbage collection', 'performance tuning', 'debugging', 'deployment', 'build automation', 'version control', 'agile', 'scrum', 'jira', 'uml', 'data structures', 'algorithms'
    ],
    'Web Development': [
        'html', 'css', 'javascript', 'react', 'node.js', 'express',
        'mongodb', 'frontend', 'backend', 'api', 'rest', 'bootstrap', 'typescript', 'next.js', 'redux', 'vue', 'angular', 'sass', 'less', 'webpack', 'babel', 'graphql', 'php', 'laravel', 'django', 'flask', 'mysql', 'sqlite', 'postgresql', 'responsive design', 'ui', 'ux', 'websockets', 'jwt', 'oauth', 'authentication', 'authorization', 'testing', 'jest', 'mocha', 'chai', 'cypress', 'storybook', 'material ui', 'tailwind', 'vercel', 'netlify', 'heroku', 'aws', 'azure', 'cloud', 'api integration', 'restful', 'soap', 'web security', 'seo', 'performance optimization', 'pwa', 'service worker', 'ssr', 'csr', 'spa', 'mvc', 'mvvm', 'git', 'github', 'bitbucket', 'agile', 'scrum', 'jira'
    ],
    'Android Development': [
        'java', 'kotlin', 'android', 'xml', 'firebase',
        'android studio', 'gradle', 'jetpack'
    ],
    'DevOps': [
        'docker', 'kubernetes', 'aws', 'azure', 'jenkins',
        'ci/cd', 'terraform', 'ansible', 'monitoring'
    ],
    'Testing': [
        'selenium', 'junit', 'pytest', 'test case',
        'testng', 'automation', 'manual testing'
    ],
    'Cloud Computing': [
        'aws', 'azure', 'gcp', 'cloud', 'lambda', 'ec2', 's3', 'devops'
    ],
    'Cyber Security': [
        'security', 'vulnerability', 'penetration testing', 'firewall',
        'encryption', 'network security'
    ],
    'Networking': [
        'tcp/ip', 'dns', 'firewall', 'vpn',
        'networking', 'routing', 'switching', 'protocols'
    ],
    'UI/UX': [
        'figma', 'wireframe', 'adobe xd', 'prototyping',
        'ui', 'ux', 'design'
    ],
    'Business Analyst': [
        'requirement gathering', 'data analysis', 'process modeling',
        'excel', 'dashboard', 'power bi', 'tableau',
        'communication', 'business process'
    ]
}


def calculate_score(resume_text: str, predicted_field: str) -> float:
    """
    Calculates the skill match score between resume content and required job field skills.
    
    Args:
        resume_text (str): The full cleaned resume text.
        predicted_field (str): The job role/domain predicted for this resume.

    Returns:
        float: A score between 0 and 100 representing how well the resume matches the field.
    """
    if not resume_text:
        print("Warning: Empty resume text.")
        return 0.0
    
    if not predicted_field:
        print("Warning: Empty predicted field.")
        return 0.0

    resume_text = resume_text.lower().strip()
    predicted_field = predicted_field.strip()

    # Retrieve skill list for the field
    skills = SKILL_KEYWORDS.get(predicted_field)
    if not skills:
        print(f"Warning: Unknown predicted field '{predicted_field}'.")
        return 0.0

    # Count matches
    matched_keywords = sum(
        1 for skill in skills if re.search(r'\b' + re.escape(skill) + r'\b', resume_text)
    )
    total_keywords = len(skills)

    # Score calculation
    score = (matched_keywords / total_keywords) * 100 if total_keywords else 0.0
    return round(score, 2)