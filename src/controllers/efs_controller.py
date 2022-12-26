from pathlib import Path

MIDDLE_FILENAME_PREFIX = "├──"
LAST_FILENAME_PREFIX = "└──"
MIDDLE_PARENT_PREFIX = "    "
LAST_PARENT_PREFIX = "│   "


class DirectoryWalker:
    def __init__(self, path, parent_path, is_last):
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last

        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    @classmethod
    def make_tree(cls, root, parent=None, is_last=False, criteria=None):
        root = Path(str(root))
        criteria = criteria or cls._default_criteria

        displayable_root = cls(root, parent, is_last)
        yield displayable_root

        children = sorted(
            list(path for path in root.iterdir() if criteria()),
            key=lambda s: str(s).lower(),
        )

        count = 1
        for path in children:
            is_last = count == len(children)

            if path.is_dir():
                yield from cls.make_tree(
                    path, parent=displayable_root, is_last=is_last, criteria=criteria
                )
            else:
                yield cls(path, displayable_root, is_last)
            count += 1

    @classmethod
    def _default_criteria(cls):
        return True

    @property
    def displayed_name(self):
        if self.path.is_dir():
            return self.path.name + "/"

        return self.path.name

    def stringify(self):
        if self.parent is None:
            return self.displayed_name

        filename_prefix = (
            LAST_FILENAME_PREFIX if self.is_last else MIDDLE_FILENAME_PREFIX
        )

        parent = self.parent
        tree_sections = [f"{str(filename_prefix)} {str(self.displayed_name)}"]
        while parent and parent.parent is not None:
            tree_sections.append(
                MIDDLE_PARENT_PREFIX if parent.is_last else LAST_PARENT_PREFIX
            )
            parent = parent.parent

        return "".join(reversed(tree_sections))


def walk_directory(path: str) -> str:
    directory_tree = DirectoryWalker.make_tree(Path(path))

    return "\n".join([tree_node.stringify() for tree_node in directory_tree])
