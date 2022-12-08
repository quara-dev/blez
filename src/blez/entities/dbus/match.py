from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class MatchRulesDef:
    type: str = "signal"
    sender: str | None = None
    interface: str | None = None
    member: str | None = None
    path: str | None = None
    path_namespace: str | None = None
    destination: str | None = None
    arg0namespace: str | None = None
    args: dict[str, str] | None = None


class MatchRules:
    """D-Bus signal match rules.
    .. seealso:: https://dbus.freedesktop.org/doc/dbus-specification.html#message-bus-routing-match-rules
    """

    def __init__(
        self,
        type: str = "signal",
        sender: str | None = None,
        interface: str | None = None,
        member: str | None = None,
        path: str | None = None,
        path_namespace: str | None = None,
        destination: str | None = None,
        arg0namespace: str | None = None,
        **kwargs: str,
    ) -> None:
        if kwargs:
            for k, v in kwargs.items():
                if re.match(r"^arg\d+$", k):
                    if not isinstance(v, str):
                        raise TypeError(f"kwarg '{k}' must have a str value")
                elif re.match(r"^arg\d+path$", k):
                    if not isinstance(v, str):
                        raise TypeError(f"Invalid object path: {v}")
                else:
                    raise ValueError("kwargs must be in the form 'arg0' or 'arg0path'")
        self.type = type
        self.args = kwargs or None
        self.arg0namespace = arg0namespace
        self.destination = destination
        self.interface = interface
        self.member = member
        self.path = path
        self.path_namespace = path_namespace
        self.sender = sender

    @classmethod
    def from_def(cls, rules: MatchRulesDef) -> MatchRules:
        options = rules.args or {}
        return cls(
            type=rules.type,
            sender=rules.sender,
            interface=rules.interface,
            member=rules.member,
            path=rules.path,
            path_namespace=rules.path_namespace,
            destination=rules.destination,
            arg0namespace=rules.arg0namespace,
            **options,
        )

    @classmethod
    def parse(cls, rules: str) -> MatchRules:
        return cls(**dict(r.split("=") for r in rules.split(",")))

    def __str__(self) -> str:
        rules = [f"type={self.type}"]

        if self.sender:
            rules.append(f"sender={self.sender}")

        if self.interface:
            rules.append(f"interface={self.interface}")

        if self.member:
            rules.append(f"member={self.member}")

        if self.path:
            rules.append(f"path={self.path}")

        if self.path_namespace:
            rules.append(f"path_namespace={self.path_namespace}")

        if self.destination:
            rules.append(f"destination={self.destination}")

        if self.args:
            for k, v in self.args.items():
                rules.append(f"{k}={v}")

        if self.arg0namespace:
            rules.append(f"arg0namespace={self.arg0namespace}")

        return ",".join(rules)

    def __repr__(self) -> str:
        return f"MatchRules({self})"
