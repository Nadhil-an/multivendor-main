from whitenoise.storage import CompressedManifestStaticFilesStorage

class CustomWhiteNoiseStorage(CompressedManifestStaticFilesStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manifest_strict = False
