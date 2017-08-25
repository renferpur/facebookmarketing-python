import hashlib
import hmac
import requests
from facebookmarketing import exception
from facebookmarketing.decorator import access_token_required
from facebookmarketing.enumerator import MethodEnum, ErrorEnum
from urllib.parse import urlencode


class Client(object):
    BASE_URL = 'https://graph.facebook.com/'

    def __init__(self, app_id, app_secret, version):
        self.app_id = app_id
        self.app_secret = app_secret
        self.version = version
        self.access_token = None
        self.BASE_URL += self.version

    def set_access_token(self, token):
        """Sets the Access Token for its use in this library.

        Args:
            token: A string with the Access Token.

        """
        self.access_token = token

    def get_app_token(self):
        """Generates an Application Token.


        Returns:
            A dict.

        """
        params = {
            'client_id': self.app_id,
            'client_secret': self.app_secret,
            'grant_type': 'client_credentials'
        }
        url = self.BASE_URL + '/oauth/access_token'
        return self._request(MethodEnum.GET, url, params=params)

    def authorization_url(self, redirect_url, scope):
        """Generates an Authorization URL.

        Args:
            redirect_url: A string with the redirect_url set in the app config.
            scope: A sequence of strings with the scopes.

        Returns:
            A string.

        """
        params = {
            'client_id': self.app_id,
            'redirect_uri': redirect_url,
            'scope': ' '.join(scope)
        }
        url = 'https://facebook.com/dialog/oauth?' + urlencode(params)
        return url

    def exchange_code(self, redirect_url, code):
        """Exchanges a code for a Token.

        Args:
            redirect_url: A string with the redirect_url set in the app config.
            code: A string containing the code to exchange.

        Returns:
            A dict.

        """
        params = {
            'client_id': self.app_id,
            'redirect_uri': redirect_url,
            'client_secret': self.app_secret,
            'code': code
        }
        url = self.BASE_URL + '/oauth/access_token'
        return self._request(MethodEnum.GET, url, params=params)

    def extend_token(self, token):
        """Extends a short-lived Token for a long-lived Token.

        Args:
            token: A string with the token to extend.

        Returns:
            A dict.

        """
        params = {
            'grant_type': 'fb_exchange_token',
            'client_id': self.app_id,
            'client_secret': self.app_secret,
            'fb_exchange_token': token
        }
        url = self.BASE_URL + '/oauth/access_token'
        return self._request(MethodEnum.GET, url, params=params)

    def inspect_token(self, input_token, token):
        """Inspects an Access Token.

        Args:
            input_token: A string with the Access Token to inspect.
            token: A string with the Developer Token (App Owner) or an Application Token.

        Returns:
            A dict.

        """
        params = {
            'input_token': input_token,
            'access_token': token
        }
        url = self.BASE_URL + '/debug_token'
        return self._request(MethodEnum.GET, url, params=params)

    def _get_params(self, token=None):
        _token = token if token else self.access_token
        return {
            'access_token': _token,
            'appsecret_proof': self._get_app_secret_proof(_token)
        }

    def _get_app_secret_proof(self, token):
        key = self.app_secret.encode('utf-8')
        msg = token.encode('utf-8')
        h = hmac.new(key, msg=msg, digestmod=hashlib.sha256)
        return h.hexdigest()

    @access_token_required
    def get_account(self):
        """Gets the authed account information.

        Returns:
            A dict.

        """
        params = self._get_params()
        url = self.BASE_URL + '/me'
        return self._request(MethodEnum.GET, url, params=params)

    @access_token_required
    def get_pages(self):
        """Gets the authed account pages.

        Returns:
            A dict.

        """
        params = self._get_params()
        url = self.BASE_URL + '/me/accounts'
        return self._request(MethodEnum.GET, url, params=params)

    @access_token_required
    def get_page_token(self, page_id):
        pages = self.get_pages()
        return next((p for p in pages['data'] if p['id'] == page_id), None)

    def get_page_subscribed_apps(self, page_id, token):
        params = self._get_params(token)
        url = self.BASE_URL + '/{}/subscribed_apps'.format(page_id)
        return self._request(MethodEnum.GET, url, params=params)

    def create_page_subscribed_apps(self, page_id, token):
        params = self._get_params(token)
        url = self.BASE_URL + '/{}/subscribed_apps'.format(page_id)
        return self._request(MethodEnum.POST, url, params=params)

    def delete_page_subscribed_apps(self, page_id, token):
        params = self._get_params(token)
        url = self.BASE_URL + '/{}/subscribed_apps'.format(page_id)
        return self._request(MethodEnum.DELETE, url, params=params)

    @access_token_required
    def get_ad_account_leadgen_forms(self, page_id):
        """Gets the forms for the given page.

        Args:
            page_id: A string with Page's ID.

        Returns:
            A dict.

        """
        params = self._get_params()
        url = self.BASE_URL + '/{}/leadgen_forms'.format(page_id)
        return self._request(MethodEnum.GET, url=url, params=params)

    @access_token_required
    def get_ad_leads(self, form_id, from_date=None):
        """Gets the leads for the given form.

        Args:
            form_id: A string with the Form's ID.
            from_date: A datetime object.

        Returns:
            A dict.

        """
        params = self._get_params()
        params['from_date'] = from_date.timestamp()
        url = self.BASE_URL + '/{}/leads'.format(form_id)
        return self._request(MethodEnum.GET, url=url, params=params)

    def create_ad_leads(self):
        raise NotImplementedError

    def get_ad_creatives(self):
        raise NotImplementedError

    def get_ad_copies(self):
        raise NotImplementedError

    def create_ad_copies(self):
        raise NotImplementedError

    def get_ad_insights(self):
        raise NotImplementedError

    def create_ad_insights(self):
        raise NotImplementedError

    def get_ad_keyword_stats(self):
        raise NotImplementedError

    def get_ad_previews(self):
        raise NotImplementedError

    def get_ad_targeting_sentence_lines(self):
        raise NotImplementedError

    def get_ad_account_activities(self):
        raise NotImplementedError

    def get_ad_account_ad_place_page_sets(self):
        raise NotImplementedError

    def create_ad_account_ad_place_page_sets(self):
        raise NotImplementedError

    def get_ad_account_ad_studies(self):
        raise NotImplementedError

    def get_ad_account_ad_asset_feeds(self):
        raise NotImplementedError

    def get_ad_account_ad_creatives(self):
        raise NotImplementedError

    def create_ad_account_ad_creatives(self):
        raise NotImplementedError

    def get_ad_account_ad_creatives_by_labels(self):
        raise NotImplementedError

    def get_ad_account_ad_images(self):
        raise NotImplementedError

    def create_ad_account_ad_images(self):
        raise NotImplementedError

    def delete_ad_account_ad_images(self):
        raise NotImplementedError

    def get_ad_account_ad_labels(self):
        raise NotImplementedError

    def create_ad_account_ad_labels(self):
        raise NotImplementedError

    def get_ad_account_ad_report_runs(self):
        raise NotImplementedError

    def get_ad_account_ad_report_schedules(self):
        raise NotImplementedError

    def get_ad_account_ad_rules_library(self):
        raise NotImplementedError

    def create_ad_account_ad_rules_library(self):
        raise NotImplementedError

    def get_ad_account_ads(self):
        raise NotImplementedError

    def create_ad_account_ads(self):
        raise NotImplementedError

    def get_ad_account_ads_by_label(self):
        raise NotImplementedError

    def get_ad_account_adsets(self):
        raise NotImplementedError

    def create_ad_account_adsets(self):
        raise NotImplementedError

    def get_ad_account_adsets_by_labels(self):
        raise NotImplementedError

    def get_ad_account_ads_pixel(self):
        raise NotImplementedError

    def create_ad_account_ads_pixel(self):
        raise NotImplementedError

    def get_ad_account_adtoplinedetails(self):
        raise NotImplementedError

    def get_ad_account_adtoplines(self):
        raise NotImplementedError

    def get_ad_account_advertisable_applications(self):
        raise NotImplementedError

    def get_ad_account_advideos(self):
        raise NotImplementedError

    def create_ad_account_advideos(self):
        raise NotImplementedError

    def get_ad_account_an_roas(self):
        raise NotImplementedError

    def get_ad_account_applications(self):
        raise NotImplementedError

    def get_ad_account_async_requests(self):
        raise NotImplementedError

    def get_ad_account_asyncadrequestsets(self):
        raise NotImplementedError

    def create_ad_account_asyncadrequestsets(self):
        raise NotImplementedError

    def get_ad_account_broadtargetingcategories(self):
        raise NotImplementedError

    def get_ad_account_business_activities(self):
        raise NotImplementedError

    def get_ad_account_campaigns(self):
        raise NotImplementedError

    def create_ad_account_campaigns(self):
        raise NotImplementedError

    def delete_ad_account_campaigns(self):
        raise NotImplementedError

    def get_ad_account_campaigns_by_label(self):
        raise NotImplementedError

    def get_ad_account_contextual_targeting_browse(self):
        raise NotImplementedError

    def get_ad_account_custom_audiences(self):
        raise NotImplementedError

    def create_ad_account_custom_audiences(self):
        raise NotImplementedError

    def get_ad_account_custom_audiencestos(self):
        raise NotImplementedError

    def get_ad_account_delivery_estimate(self):
        raise NotImplementedError

    def get_ad_account_generate_previews(self):
        raise NotImplementedError

    def get_ad_account_insights(self):
        raise NotImplementedError

    def create_ad_account_insights(self):
        raise NotImplementedError

    def get_ad_account_instagram_accounts(self):
        raise NotImplementedError

    def get_ad_account_minimum_budgets(self):
        raise NotImplementedError

    def get_ad_account_offline_conversion_data_sets(self):
        raise NotImplementedError

    def get_ad_account_offsitepixels(self):
        raise NotImplementedError

    def create_account_ad_offsitepixels(self):
        raise NotImplementedError

    def get_ad_account_partnercategories(self):
        raise NotImplementedError

    def get_ad_account_partners(self):
        raise NotImplementedError

    def get_ad_account_publisher_block_lists(self):
        raise NotImplementedError

    def create_ad_account_publisher_block_lists(self):
        raise NotImplementedError

    def get_ad_account_ratecard(self):
        raise NotImplementedError

    def get_ad_account_reachestimate(self):
        raise NotImplementedError

    def get_ad_account_reach_frequency_predictions(self):
        raise NotImplementedError

    def create_ad_account_reach_frequency_predictions(self):
        raise NotImplementedError

    def get_ad_account_roas(self):
        raise NotImplementedError

    def get_ad_account_rule_execution_history(self):
        raise NotImplementedError

    def get_ad_account_targeting_browse(self):
        raise NotImplementedError

    def get_ad_account_targeting_search(self):
        raise NotImplementedError

    def get_ad_account_targeting_sentence_lines(self):
        raise NotImplementedError

    def get_ad_account_targeting_suggestions(self):
        raise NotImplementedError

    def get_ad_account_targeting_validations(self):
        raise NotImplementedError

    def get_ad_account_targeting_tracking(self):
        raise NotImplementedError

    def create_ad_account_targeting_tracking(self):
        raise NotImplementedError

    def delete_ad_account_targeting_tracking(self):
        raise NotImplementedError

    def get_ad_account_targeting_transactions(self):
        raise NotImplementedError

    def get_ad_account_users(self):
        raise NotImplementedError

    # TODO Endpoints
    # Ad
    # Creative
    # Ad
    # Image
    # Ad
    # Previews
    # Ad
    # Preview
    # Plugin
    # Ad
    # Set
    # Ad
    # User
    # Ad
    # Video
    # Campaign
    # Connection
    # Objects
    # Currencies
    # Image
    # Crop
    # Product
    # Catalog

    def _request(self, method, url, params=None, data=None):
        response = requests.request(method.value, url, params=params, data=data)
        return self._parse(response.json())

    def _parse(self, response):
        if 'error' in response:
            error = response['error']
        elif 'data' in response and 'error' in response['data']:
            error = response['data']['error']
        else:
            error = None

        if error:
            code = error['code']
            message = error['message']
            try:
                error_enum = ErrorEnum(code)
            except Exception:
                raise exception.UnexpectedError('Error: {}. Message {}'.format(code, message))
            if error_enum == ErrorEnum.UnknownError:
                raise exception.UnknownError(message)
            elif error_enum == ErrorEnum.AppRateLimit:
                raise exception.AppRateLimitError(message)
            elif error_enum == ErrorEnum.AppPermissionRequired:
                raise exception.AppPermissionRequiredError(message)
            elif error_enum == ErrorEnum.UserRateLimit:
                raise exception.UserRateLimitError(message)
            elif error_enum == ErrorEnum.InvalidParameter:
                raise exception.InvalidParameterError(message)
            elif error_enum == ErrorEnum.SessionKeyInvalid:
                raise exception.SessionKeyInvalidError(message)
            elif error_enum == ErrorEnum.IncorrectPermission:
                raise exception.IncorrectPermissionError(message)
            elif error_enum == ErrorEnum.InvalidOauth20AccessToken:
                raise exception.PermissionError(message)
            elif error_enum == ErrorEnum.ExtendedPermissionRequired:
                raise exception.ExtendedPermissionRequiredError(message)
            else:
                raise exception.BaseError('Error: {}. Message {}'.format(code, message))

        return response
