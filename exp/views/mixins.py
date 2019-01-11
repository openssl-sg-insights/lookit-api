from guardian.mixins import LoginRequiredMixin
from django.conf import settings
from studies.models import StudyType

import requests


# TODO: Using a mixin for this stuff is overkill. All of this functionality should be migrated
# to helper functions.


class ExperimenterLoginRequiredMixin(LoginRequiredMixin):
    login_url = settings.EXPERIMENTER_LOGIN_URL


class StudyTypeMixin:

    def validate_and_fetch_metadata(self):
        """Gets the study type and runs hardcoded validations.

        TODO: this is obviously a fragile pattern, and there's probably a better way to do this.
            Let's think of a way to do this more dynamically in the future.

        :return: A tuple of boolean and tuple, the inner tuple containing error data.
        """
        study_type = StudyType.objects.get(id=self.request.POST.get('study_type'))
        metadata = self.extract_type_metadata(study_type=study_type)

        errors = VALIDATIONS.get(study_type.name, is_valid_ember_frame_player)(metadata)

        return metadata, errors

    def extract_type_metadata(self, study_type=None):
        """
        Pull the metadata related to the selected StudyType from the POST request
        """
        if not study_type:
            study_type = StudyType.objects.get(id=self.request.POST.get('study_type'))

        type_fields = study_type.configuration['metadata']['fields']

        metadata = {}

        for key in type_fields:
            metadata[key] = self.request.POST.get(key, None)

        return metadata


def is_valid_ember_frame_player(metadata):
    """Checks commit shas and addons repo url.

    This must fulfill the contract of returning a list. We are exploiting the fact that empty
    lists evaluate falsey.

    :param metadata: the metadata object containing shas for both frameplayer and addons repo
    :type metadata: dict
    :return: a list of errors.
    :rtype: list.
    """
    addons_repo_url = metadata.get('addons_repo_url', settings.EMBER_ADDONS_REPO)
    frameplayer_commit_sha = metadata.get('last_known_player_sha', '')
    addons_commit_sha = metadata.get('last_known_addons_sha', '')

    errors = []

    if not requests.get(addons_repo_url).ok:
        errors.append(f'Addons repo url {addons_repo_url} does not work.')
    if not requests.get(f'{settings.EMBER_EXP_PLAYER_REPO}/commit/{frameplayer_commit_sha}').ok:
        errors.append(f'Frameplayer commit {frameplayer_commit_sha} does not exist.')
    if not requests.get(f'{settings.EMBER_ADDONS_REPO}/commit/{addons_commit_sha}').ok:
        errors.append(f'Addons commit {addons_commit_sha} does not exist.')

    return errors


VALIDATIONS = {
    'Ember Frame Player (default)': is_valid_ember_frame_player
}
