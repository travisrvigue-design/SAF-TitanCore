from scripts.partitioner import partition_fastq


def test_partitioner_deterministic(tmp_path):
    input_file = tmp_path / "test.fastq"
    input_file.write_text("""@r1\nA\n+\n~\n@r2\nC\n+\n~\n""")
    out = tmp_path / "units"
    manifest1 = partition_fastq(str(input_file), str(out), chunk_lines=2)
    manifest2 = partition_fastq(str(input_file), str(out), chunk_lines=2)
    assert manifest1['units'][0]['sha256'] == manifest2['units'][0]['sha256']
