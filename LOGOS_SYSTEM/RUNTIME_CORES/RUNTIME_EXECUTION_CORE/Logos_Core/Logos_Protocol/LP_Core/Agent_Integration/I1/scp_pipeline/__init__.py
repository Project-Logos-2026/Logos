from .pipeline_runner import PipelineRunner, run_scp_pipeline


class SCPPipeline:
	def __init__(self, *args, **kwargs):
		self.runner = PipelineRunner()

	def run(self, *args, **kwargs):
		return self.runner.run(lambda: None, ticks=1)
