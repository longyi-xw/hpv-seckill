def handle_exceptions(cls):
    class DecoratedClass(cls):
        def __getattribute__(self, name: str):
            method = super().__getattribute__(name)
            if callable(method) and not name.startswith(f"_{cls.__name__}__"):
                def wrapper(*args, **kwargs):
                    response = ""
                    try:
                        response = method(*args, **kwargs)
                        if not response: return
                        if type(response) == dict and response.get('code'):
                            message = ""
                            if response.get("code") == '0000':
                                for k, v in response.items():
                                    if k == 'data':
                                        return v
                            else:
                                message = response.get('msg')
                                print(f"[Method:{cls.__name__}.{name}] --------> {message}")
                        return response
                    except KeyError as e:
                        print(f"[Method:{cls.__name__}.{name}] --------> KeyError Not Found: {e} {response}")
                        exit(0)

                return wrapper
            return method

    return DecoratedClass
