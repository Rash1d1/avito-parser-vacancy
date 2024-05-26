from dataclasses import dataclass

@dataclass
class ParsedItem:
    id: str 
    title: str 
    url: str 
    min_salary: str 
    max_salary: str 
    currency: str 
    salary_schedule: str 
    schedule: str 
    experience: str 
    description: str 
    employer: str 
    link_to_employer: str 
    location: str 
    date_of_publication: str