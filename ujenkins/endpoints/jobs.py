import json

from typing import Dict


class Jobs:

    def __init__(self, jenkins):
        self.jenkins = jenkins

    def _get_all_jobs(self, url: str, parent: str) -> Dict[str, dict]:

        def callback(response) -> dict:
            all_jobs = {}

            jobs = json.loads(response.body)['jobs']

            for job in jobs:
                all_jobs[parent + job['name']] = job

                # TODO: async adapter recursive calls
                # if 'Folder' in job.get('_class', ''):
                #     all_jobs.update(await self._get_all_jobs(
                #         job['url'],
                #         parent + job['name'] + '/'
                #     ))

            return all_jobs

        return self.jenkins._request('GET', url + '/api/json', callback=callback)

    def get(self) -> Dict[str, dict]:
        """
        Get dict of all existed jobs in system, including jobs in folder.

        Example:

        .. code-block:: python

            {
                'test': {
                    'name': 'test',
                    'url': 'http://localhost/job/test/'
                },
                'folder/foo': {
                    'name': 'folder/job',
                    'url': 'http://localhost/job/folder/job/foo/'
                }
            }

        Returns:
            Dict[str, dict]: name and job properties.
        """
        return self._get_all_jobs('', '')
