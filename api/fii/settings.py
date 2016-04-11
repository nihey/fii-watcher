from fii.config import Config as DefaultConfig

try:
    from fii.localconfig import Config as LocalConfig
except ImportError:
    class Config(DefaultConfig):
        pass
else:
    class Config(LocalConfig, DefaultConfig):
        pass
