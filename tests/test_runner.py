from herdr_compose.models import LayoutConfig
from herdr_compose.runner import HerdrRunner


def test_dry_run_execution(capsys):
    data = {
        "workspaces": [
            {
                "name": "project_alpha",
                "root": "/home/user/alpha",
                "focus": True,
                "tabs": [
                    {
                        "label": "code",
                        "panes": [
                            {"command": "nvim", "focus": True},
                            {
                                "direction": "right",
                                "size": 0.8,
                                "command": "cargo run",
                                "from": "root",
                            },
                        ],
                    }
                ],
            }
        ]
    }
    config = LayoutConfig.from_dict(data)

    runner = HerdrRunner(dry_run=True)
    runner.apply_layout(config)

    captured = capsys.readouterr().out
    assert "[DRY-RUN] herdr workspace create --label project_alpha --cwd /home/user/alpha --focus" in captured
    assert "[DRY-RUN] herdr tab rename w1:t1 code" in captured
    assert "[DRY-RUN] herdr pane run w1:p1 nvim" in captured
    # size in YAML is 0.8 (80%) for new pane -> herdr CLI gets 1.0 - 0.8 = 0.2
    assert "[DRY-RUN] herdr pane split w1:p1 --direction right --ratio 0.2 --cwd /home/user/alpha --no-focus" in captured
    assert "[DRY-RUN] herdr pane run w1:t1:p2 cargo run" in captured


def test_pane_level_cwd_resolution(capsys):
    data = {
        "workspaces": [
            {
                "name": "docsMCP",
                "root": "/home/user/docsmcp",
                "tabs": [
                    {
                        "label": "editor",
                        "panes": [{"command": "nvim"}],
                    },
                    {
                        "label": "watch server",
                        "panes": [
                            {"cwd": "/home/user/crabbase", "command": "make watch"}
                        ],
                    },
                ],
            }
        ]
    }
    config = LayoutConfig.from_dict(data)

    runner = HerdrRunner(dry_run=True)
    runner.apply_layout(config)

    captured = capsys.readouterr().out
    assert "[DRY-RUN] herdr workspace create --label docsMCP --cwd /home/user/docsmcp --no-focus" in captured
    assert "[DRY-RUN] herdr tab create --workspace w1 --cwd /home/user/crabbase --label watch server" in captured
    assert "[DRY-RUN] herdr pane run w1:t2:p1 make watch" in captured
