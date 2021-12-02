
INSTRUCTIONS = [
    "MAINTAINER",
    "RUN",
    "CMD",
    "ENTRYPOINT",
    "LABEL",
    "EXPOSE",
    "ENV",
    "ADD",
    "COPY",
    "VOLUME",
    "USER",
    "WORKDIR",
    "ARG",
    "ONBUILD",
    "STOPSIGNAL",
    "HEALTHCHECK",
    "SHELL",
    "#"
]

class Const(object):
    def __init__(self):
        """
            予約語
        """
        self._book = [
            NL,
            AND,
            BACK,
            BACKLEFT,
            BACKRIGHT,
            BACKNT,
            LEFT,
            RIGHT,
            SUBLEFT,
            SUBRIGHT,
        ]
    @property
    def book(self):
        return self._book