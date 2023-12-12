import functools
import os
import shutil
from zipfile import ZipFile
import subprocess

from release_build_classes import ReleaseBuildArguments, JobStage, ReleaseBuildConstants, ReleaseBuildArgumentsFactory, ArgumentParserFactory
from release_build_utilty_methods import (
    extract_zip_file,
    download_zip_and_return_file_path,
    copy_file_and_return_file_path,
    is_string_in_file_content,
)

printf = functools.partial(print, flush=True)


def _parse_arguments_from_command_line_arguments() -> ReleaseBuildArguments:
    argument_parser = ArgumentParserFactory.create_instance()
    command_line_arguments = vars(argument_parser.parse_args())

    return ReleaseBuildArgumentsFactory().create_instance_from_dictionary(command_line_arguments)


def execute_stage_check_out_and_aggregate_data_for_end_to_end_test(release_build_arguments: ReleaseBuildArguments):
    if not os.path.exists(ReleaseBuildConstants.PATH_TO_END_TO_END_TEST_CALLS_FOLDER):
        raise Exception(
            f"Folder {os.path.abspath(ReleaseBuildConstants.PATH_TO_END_TO_END_TEST_CALLS_FOLDER)} does not exist but was expected to. "
            f"Did you check out the end-to-end test tool?"
        )

    shutil.rmtree(ReleaseBuildConstants.PATH_TO_END_TO_END_TEST_CALLS_FOLDER)
    printf("Deleted folder: ", os.path.abspath(ReleaseBuildConstants.PATH_TO_END_TO_END_TEST_CALLS_FOLDER))

    zip_file_path_locally_copied_samples_db = copy_file_and_return_file_path(
        source_path=release_build_arguments.path_to_samples_db_on_jenkins, target_directory=ReleaseBuildConstants.DATABASE_DIRECTORY
    )
    extract_zip_file(zip_file_path_locally_copied_samples_db, target_directory=ReleaseBuildConstants.DATABASE_DIRECTORY)
    printf(f"Copied and extracted end-to-end test database to {os.path.abspath(ReleaseBuildConstants.DATABASE_DIRECTORY)}")

    zip_file_path_viriato_standard_nightly_stable_test = download_zip_and_return_file_path(
        url=release_build_arguments.url_viriato_standard_test_zip,
        filename=release_build_arguments.zip_file_name_viriato_standard_nightly_stable_test,
        target_directory=release_build_arguments.unzip_directory_viriato_nightly_stable,
    )
    extract_zip_file(
        path_zip_file=zip_file_path_viriato_standard_nightly_stable_test, target_directory=release_build_arguments.unzip_directory_viriato_nightly_stable
    )
    printf("Downloaded and extracted viriato to ", release_build_arguments.unzip_directory_viriato_nightly_stable)

    shutil.copytree(release_build_arguments.root_directory_call_jsons, ReleaseBuildConstants.PATH_TO_END_TO_END_TEST_CALLS_FOLDER)
    printf("Copied call json files from nightly stable to end-to-end test tool.")


def execute_stage_performing_end_to_end_test(release_build_arguments: ReleaseBuildArguments) -> None:
    if not os.path.isfile(release_build_arguments.file_path_wheel_py_client):
        raise Exception(
            f"The file {os.path.abspath(release_build_arguments.file_path_wheel_py_client)} does not exist but was expected to. "
            f"Did you prepare it in your locale directory?"
        )

    printf("Start end_to_end_tests_tool. The following output is from the end_to_end_tests_tool:")
    # the following process will be executed in the algorithmPlatform.pyclient.endtoendtesttool directory
    # so that all relatives path in this batch script: EXECUTABLE_END_TO_END_TESTS are still working without modification
    # TODO VPLAT-10906: Derive paths correctly for end2end test tool script
    process_result_end_to_end_tests = subprocess.run(
        [
            ReleaseBuildConstants.PATH_TO_EXECUTABLE_END_TO_END_TESTS,
            str(ReleaseBuildConstants.UPDATE_PIP_IN_END_TO_END_TESTS_PYTHON_ENVIRONMENT).lower(),
            os.path.join("..", release_build_arguments.file_path_wheel_py_client),
            os.path.join("..", release_build_arguments.unzip_directory_viriato_nightly_stable),
            os.path.join(ReleaseBuildConstants.DATABASE_DIRECTORY, ReleaseBuildConstants.FILE_NAME_SAMPLES_DATABASE),
            os.path.join("..", ReleaseBuildConstants.PATH_TO_END_TO_END_TEST_REPORT_FILE),
        ],
        shell=True,
        cwd=ReleaseBuildConstants.FOLDER_NAME_END_TO_END_TESTS_TOOL_ROOT,
    )
    if process_result_end_to_end_tests.returncode != 0:
        raise Exception(
            f"end_to_end_tests_tool threw an Error. Location: {ReleaseBuildConstants.PATH_TO_EXECUTABLE_END_TO_END_TESTS}. Arguments used: {process_result_end_to_end_tests.args}"
        )
    printf("End_to_end_tests_tool finished executing.")

    if not os.path.isfile(ReleaseBuildConstants.PATH_TO_END_TO_END_TEST_REPORT_FILE):
        raise Exception(
            f"The end_to_end_tests_tool report file at {os.path.abspath(ReleaseBuildConstants.PATH_TO_END_TO_END_TEST_REPORT_FILE)} does not exist"
            f"but was expected to be created by the end_to_end_tests_tool. "
        )

    if not is_string_in_file_content(
        search_string=ReleaseBuildConstants.SUCCESS_STRING_OF_END_TO_END_TESTS_TOOL, file_path=ReleaseBuildConstants.PATH_TO_END_TO_END_TEST_REPORT_FILE
    ):
        raise Exception(
            f"The end_to_end_tests_tool report file at {os.path.abspath(ReleaseBuildConstants.PATH_TO_END_TO_END_TEST_REPORT_FILE)} "
            f"shows that the End_to_end_tests_tool failed."
        )

    printf("The End_to_end_tests_tool was executed successfully. There are no errors and no test fails.")


def execute_stage_preparing_artifacts(release_build_arguments: ReleaseBuildArguments) -> None:
    if not os.path.isfile(ReleaseBuildConstants.FILE_PATH_LICENSES_PY_CLIENT):
        raise Exception(f"LICENSE File {os.path.abspath(ReleaseBuildConstants.FILE_PATH_LICENSES_PY_CLIENT)} does not exist but was expected to.")
    if not os.path.isfile(release_build_arguments.file_path_wheel_py_client):
        raise Exception(f"WHEEL FILE {os.path.abspath(release_build_arguments.file_path_wheel_py_client)} does not exist but was expected to.")

    zip_file_path_algorithm_research_package = download_zip_and_return_file_path(
        url=release_build_arguments.release_url_algorithm_platform_research,
        filename=release_build_arguments.zip_file_name_algorithm_platform_research_release,
        target_directory=ReleaseBuildConstants.OUTPUT_DIRECTORY,
    )
    printf("Downloaded the following zip: ", zip_file_path_algorithm_research_package)

    if not os.path.isfile(zip_file_path_algorithm_research_package):
        # We need to validate that the file was really successfully downloaded
        # because the next call would create a new zip file and the error would be difficult to spot.
        raise FileNotFoundError("Cannot find AlgorithmResearch_Package*.zip in: ", zip_file_path_algorithm_research_package)

    with ZipFile(zip_file_path_algorithm_research_package, "a") as algorithm_zip:
        algorithm_zip.write(
            filename=release_build_arguments.file_path_wheel_py_client, arcname=os.path.basename(release_build_arguments.file_path_wheel_py_client)
        )
        printf(f"Added file:{release_build_arguments.file_path_wheel_py_client} to the already existing zip: {zip_file_path_algorithm_research_package}.")

        algorithm_zip.write(
            filename=ReleaseBuildConstants.FILE_PATH_LICENSES_PY_CLIENT, arcname=os.path.basename(ReleaseBuildConstants.FILE_PATH_LICENSES_PY_CLIENT)
        )
        printf(f"Added file:{ReleaseBuildConstants.FILE_PATH_LICENSES_PY_CLIENT} to the already existing zip: {zip_file_path_algorithm_research_package}.")


def main():
    release_build_arguments = _parse_arguments_from_command_line_arguments()

    printf(f"Stage: {release_build_arguments.job_stage}")
    printf(
        f"Release branch: '{release_build_arguments.release_branch_py_client}' and py_client Wheel-name: '{release_build_arguments.file_path_wheel_py_client}'"
    )

    match release_build_arguments.job_stage:
        case JobStage.prepare_artifacts:
            execute_stage_preparing_artifacts(release_build_arguments=release_build_arguments)
        case JobStage.check_out_and_aggregate_data_for_end_to_end_test:
            execute_stage_check_out_and_aggregate_data_for_end_to_end_test(release_build_arguments=release_build_arguments)
        case JobStage.perform_end_to_end_test:
            execute_stage_performing_end_to_end_test(release_build_arguments=release_build_arguments)
        case _:
            raise NotImplementedError(f"The step {release_build_arguments.job_stage} is not implemented.")

    printf(f"Stage: {release_build_arguments.job_stage} successfully executed.")


if __name__ == "__main__":
    main()
