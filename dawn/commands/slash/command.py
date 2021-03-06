from __future__ import annotations

import typing as t

import hikari

if t.TYPE_CHECKING:

    from dawn.extensions import Extension

from dawn.commands.slash.base import Option, SlashCallable

__all__: t.Tuple[str, ...] = ("SlashCommand",)


class SlashCommand(SlashCallable):

    """
    This object represents a discord slash command.

    Parameters
    ----------

        name: :class:`str`
            Name of the command.

        description: :class:`str`
            Description of the command.

        guild_ids: :class:`Sequence[int]`
            List of guild ids this command is bound to.

        options: :class:`Tuple[Option, ...]`
            A tuple of command options.

    """

    __slots__: t.Tuple[str, ...] = (
        "_extension",
        "_name",
        "_description",
        "_guild_ids",
        "_options",
    )

    def __init__(
        self,
        name: str,
        description: str,
        guild_ids: t.Sequence | None = None,
        options: t.Tuple[Option, ...] = (),
    ) -> None:
        self._extension: Extension | None = None
        self._name = name.lower()
        self._description = description
        self._guild_ids = guild_ids or []
        self._options = options
        super().__init__()

    @property
    def name(self) -> str:
        """Name of the command."""
        return self._name

    @property
    def description(self) -> str:
        """Description fo the command."""
        return self._description

    @property
    def guild_ids(self) -> t.Sequence[int]:
        """Sequence of guild_ids this command is bound to."""
        return self._guild_ids

    @property
    def options(self) -> t.Tuple[Option, ...]:
        """Tuple of command options"""
        return self._options

    @property
    def extension(self) -> Extension | None:
        """Extension which is binded with this command"""
        return self._extension

    def autocomplete(
        self, option_name: str, /
    ) -> t.Callable[
        [
            t.Callable[
                [hikari.AutocompleteInteraction, hikari.AutocompleteInteractionOption],
                t.Awaitable[t.Any],
            ]
        ],
        None,
    ]:
        """Add autocomplete for a command option.

        Parameters
        ----------

            option_name: :class:`str`
                Name of the option this autocomplete is for.

        Example
        -------

            >>> @bot.slash
            >>> @dawn.slash_command(options=[dawn.Option("color", autocomplete=True)])
            >>> async def colors(ctx: dawn.SlashContext, color: str) -> None:
            >>>     await ctx.create_response(f"{ctx.author} chose {color}")
            >>>
            >>> @colors.autocomplete("color")
            >>> async def ac_color(inter: hikari.AutocompleteInteraction, option: hikari.AutocompleteInteractionOption) -> list[hikari.CommandChoice| str]:
            >>>       return [
            >>>         "red",
            >>>         hikari.CommandChoice(name="blue", value="blue")
            >>>     ]

        """
        return super().autocomplete(option_name)

    def _compare_with(self, command: hikari.SlashCommand) -> bool:
        return (
            self.name == command.name
            and self.description == command.description
            and len(self.options) == len(command.options or [])
            and all(
                (option.name, option.description, option.type)
                == (option_c.name, option_c.description, option.type)
                for option, option_c in zip(self.options, command.options or [])
            )
        )
