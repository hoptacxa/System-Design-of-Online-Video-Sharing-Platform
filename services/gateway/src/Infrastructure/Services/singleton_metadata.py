class SingletonMeta(type):
    """
    A metaclass for implementing the Singleton pattern.
    Ensures only one instance of the class exists.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # Create the instance and store it in the _instances dictionary
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
