from .pipeline_runner import PipelineRunner, run_mtp_pipeline


class MTPPipeline:
    def __init__(self, *args, **kwargs):
        self.runner = PipelineRunner()

    def run(self, *args, **kwargs):
        return self.runner.run(lambda: None, ticks=1)
