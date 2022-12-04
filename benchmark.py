from typing import Any

from main import parser
from amoeba_game import AmoebaGame


class GameConfig:

	base_args = ['-l', '500', '-p', '4', '--no_vid']

	def _add_opt(self, opt: str, val: Any):
		self.base_args.extend([opt, str(val)])
		return self

	def add_player(self, player: int):
		self._add_opt('-p', player)
		return self

	def add_metabolism(self, metabolism: float):
		self._add_opt('-m', metabolism)
		return self

	def add_size(self, size: int):
		self._add_opt('-A', size)
		return self

	def add_density(self, density: float):
		self._add_opt('-d', density)
		return self

	def get_args(self) -> list:
		return self.base_args


test_config = GameConfig()
(test_config
	.add_player(4)
	.add_metabolism(1)
	.add_size(5)
	.add_density(0.2)
)

args = parser.parse_args(test_config.get_args())
AmoebaGame(args)