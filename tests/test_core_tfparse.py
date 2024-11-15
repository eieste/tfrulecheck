# -*- coding: utf-8 -*-
import hcl2

from tfutility.core.tffile import OpendTfFile, TfBlock, TfFile


def test_filemetadata_extract_blocks_simple(mocker):
    mocker.patch("tfutility.core.tffile.TfFile.read_tf")
    fm = TfFile("")

    fm._extract_blocks(
        {
            "terraform": [
                {
                    "required_providers": [
                        {"aws": "fooo", "__start_line__": 5, "__end_line__": 5}
                    ],
                    "__start_line__": 1,
                    "__end_line__": 5,
                }
            ]
        },
        "",
    )
    targets = ["terraform.required_providers"]
    assert all([block.id in targets for block in fm._blocks])


def test_filemetadata_extract_blocks_more(mocker):
    mocker.patch("tfutility.core.tffile.TfFile.read_tf")
    fm = TfFile("")

    with open("./tests/testcode/main.tf", "r") as fobj:
        data = hcl2.load(fobj, with_meta=True)

    fm._extract_blocks(data, "")
    targets = [
        "terraform.required_providers",
        "provider.aws",
        "resource.aws_s3_bucket.example",
        "resource.aws_s3_bucket_object.object2",
        "module.testmodule_localsource.source",
        "module.testmodule_remotesource.source",
        "moved",
    ]
    print(fm._blocks)
    assert all([block.id in targets for block in fm._blocks])


def test_find_decorators_nothing_found(mocker):
    mocker.patch(
        "tfutility.core.tffile.TfFile.read_tf",
        return_value=OpendTfFile(None, ["a", "b", "c", "d"], None),
    )
    tff = TfFile("", autoparse=False)
    bw = TfBlock(tff, "foo", {"__start_line__": 5, "__end_line__": 5})
    assert bw._find_decorators() == []


def test_find_decorators_found(mocker):
    mocker.patch(
        "tfutility.core.tffile.TfFile.read_tf",
        return_value=OpendTfFile(
            None,
            ['# @bar(bar="test")', "a", '# @fooo(bar="test", party="hard")', "c", "d"],
            None,
        ),
    )
    tff = TfFile("", autoparse=False)
    nbw = TfBlock(tff, "foo", {"__start_line__": 4, "__end_line__": 5})
    x = nbw._find_decorators()
    assert x[0].name == "fooo"
    assert len(x) == 1
    assert x[0].parameter("bar") == "test"
    assert x[0].parameter("party") == "hard"
