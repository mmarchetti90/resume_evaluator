#!/bin/bash python3

### IMPORTS -------------------------------- ###

import requests

from bs4 import BeautifulSoup

### CLASSES -------------------------------- ###

class Job:
    
    """
    Class for retrieving a job from LinkedIn or loading it from file
    """

    def __init__(self) -> None:
        
        pass
    
    ### ------------------------------------ ###
    
    def parse(self, job_uri: str) -> tuple[bool, str]:
        
        if job_uri.startswith('https://'):
            ok_signal, error_msg = self.parse_linkedin_url(job_uri)
        elif job_uri.endswith('.md') or job_uri.endswith('.txt'):
            ok_signal, error_msg = self.parse_md(job_uri)
        else:
            return False, 'ERROR: invalid job uri'
        
        return ok_signal, error_msg
    
    ### ------------------------------------ ###
    
    def parse_linkedin_url(self, url: str) -> tuple[bool, str]:
        
        """
        Parses a url link to a LinkedIn job
        """

        # Init job details dict
        self.job_details = {
            'title': None,
            'company': None,
            'location': None,
            'link': url,
            'description': None,
            'time': None,
            'seniority_level': None,
            'industry': None,
            'employment_type': None,
            'job_function': None
        }

        # Get the job details
        response = requests.get(url)
        if response.status_code != 200:
            return False, f'ERROR: requests status code {response.status_code}'
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Title
            try:
                self.job_details['title'] = soup.find("div",{"class":"top-card-layout__entity-info"}).find("a").text.strip()
            except:
                pass
            # Company name
            try:
                self.job_details['company'] = soup.find('a', {'class': 'topcard__org-name-link'}).text.strip()
            except:
                pass
            # Location
            try:
                self.job_details['location'] = soup.select_one('h4.top-card-layout__second-subline > div.topcard__flavor-row > span.topcard__flavor.topcard__flavor--bullet').text.strip()
            except:
                pass
            # Time posted
            try:
                self.job_details['time'] = soup.select_one('.posted-time-ago__text').text.strip()
            except:
                pass
            # Description
            try:
                self.job_details['description'] = soup.select_one('.show-more-less-html__markup.show-more-less-html__markup--clamp-after-5').text.strip()
            except:
                pass
            # Additional details (level, industry, type, function)
            try:
                soup_key_to_details_key = {
                    'Seniority level': 'seniority_level',
                    'Industries': 'industry',
                    'Employment type': 'employment_type',
                    'Job function': 'job_function'
                }
                job_criteria = soup.select('li.description__job-criteria-item')
                for jc in job_criteria:
                    field= jc.select_one('.description__job-criteria-subheader').text.strip()
                    self.job_details[soup_key_to_details_key[field]] = jc.select_one('.description__job-criteria-text').text.strip()
            except:
                pass

        return True, ''
    
    ### ------------------------------------ ###
    
    def parse_md(self, path: str) -> tuple[bool, str]:
        
        """
        Parses a markdown file with job info
        
        File must have the following structure
        # [Job title] (first line)
        ## COMPANY:
        ## DESCRIPTION:
        """

        # Read doc
        try:
            job_raw = open(path, 'r').read()
        except:
            return False, f'ERROR: could not open {path}'
        
        # Init job details dict
        self.job_details = {
            'title': None,
            'company': None,
            'location': None,
            'link': None,
            'description': None,
            'time': None,
            'seniority_level': None,
            'industry': None,
            'employment_type': None,
            'job_function': None,
        }
        
        # Check header line for candidate's name
        self.job_details['title'] = job_raw.split('\n')[0].replace('#', '').strip()

        # Required subheaders
        subheaders = {
            '## COMPANY:' : 'company',
            '## DESCRIPTION:' : 'description'
        }

        # Parse sections
        for section in job_raw.split('##')[1:]:
           section = '##' + section
           subh = section.split('\n')[0].strip()
           if subh in subheaders.keys():
               self.job_details[subheaders[subh]] = section.replace(subh, '').strip()

        return True, ''

### MAIN ------------------------------------ ###

if __name__ == "__main__":

    # Import args
    from sys import argv
    resume_path = argv[argv.index('--resume') + 1]

    # Parse
    job_info = Job()
    ok_signal, error_msg = job_info.parse_resume(resume_path)

    # Print
    if ok_signal:
        for key, value in job_info.job_details.items():
            print('## ' + key + ':\n' + value)
    else:
        print(error_msg)
