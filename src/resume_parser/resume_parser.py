#!/bin/bash python3

### CLASSES -------------------------------- ###

class Resume:

    """
    Class for parsing a markdown resume and storing its info
    """

    ### ------------------------------------ ###

    def __init__(self) -> None:

        pass
    
    ### ------------------------------------ ###

    def parse(self, path: str) -> tuple[bool, str]:

        """
        Reads a resume and extracts its info

        File must have the following structure
        # [Candidate name] (first line)
        ## CONTACT INFO:
        ## SUMMARY:
        ## WORK EXPERIENCE:
        ## SKILLS:
        ## EDUCATION:
        ## PUBLICATIONS:
        """

        # Read doc
        try:
            resume_raw = open(path, 'r').read()
        except:
            return False, f'ERROR: could not open {path}'
        
        # Init candidate info dict
        self.candidate_info = {}
        
        # Check header line for candidate's name
        self.candidate_info['candidate_name'] = resume_raw.split('\n')[0].replace('#', '').strip()

        # Required subheaders
        subheaders = {
            '## CONTACT INFO:' : 'contact_info',
            '## SUMMARY:' : 'summary',
            '## WORK EXPERIENCE:' : 'work_experience',
            '## SKILLS:' : 'skills',
            '## EDUCATION:' : 'education',
            '## PUBLICATIONS:' : 'publications'
        }

        # Parse sections
        for section in resume_raw.split('##')[1:]:
           section = '##' + section
           subh = section.split('\n')[0].strip()
           if subh in subheaders.keys():
               self.candidate_info[subheaders[subh]] = section.replace(subh, '').strip()

        return True, ''

### MAIN ----------------------------------- ###

if __name__ == "__main__":
    
    # Import args
    from sys import argv
    resume_path = argv[argv.index('--resume') + 1]

    # Parse
    candidate_resume = Resume()
    ok_signal, error_msg = candidate_resume.parse(resume_path)

    # Print
    if ok_signal:
        for key, value in candidate_resume.candidate_info.items():
            print('## ' + key + ':\n' + value)
    else:
        print(error_msg)
