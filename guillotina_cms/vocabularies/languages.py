from guillotina.schema.vocabulary import SimpleVocabulary


KIND_OF_AUTH = SimpleVocabulary.fromValues([
    'saml',
    'login',
    'token',
    'oauth'
])