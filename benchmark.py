import sys
from typing import Any

from main import parser
from amoeba_game import AmoebaGame


# -----------------------------------------------------------------------------
# 	Helpers
# -----------------------------------------------------------------------------

# Suppress stdout
# https://stackoverflow.com/questions/2828953/silence-the-stdout-of-a-function-in-python-without-trashing-sys-stdout-and-resto
class DummyFile(object):
    def write(self, x):
        pass

    def flush(self):
        pass


# -----------------------------------------------------------------------------
# 	Game Configuration
# -----------------------------------------------------------------------------

class GameConfig:

	base_args = ['-ng', '-l', '500', '-p', '4', '--no_vid']

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


def create_config(
	player: int,
	size: int,
	density: float,
	metabolism: float
) -> GameConfig:
	return (
		GameConfig()
			.add_player(player)
			.add_size(size)
			.add_density(density)
			.add_metabolism(metabolism)
	)


# -----------------------------------------------------------------------------
# 	Benchmarking methods
# -----------------------------------------------------------------------------

def run(config: GameConfig) -> tuple[bool, int, float]:
	"""Runs the simulator for the given game configuration, and returns
	the results.
	
	Returns:
	  ok: True if ameoba reached the goal size, otherwise False.
	  turns: # turns taken to complete the game or tried but failed.
	  ts: cpu time in seconds taken for the game.
	"""
	# suppress stdout
	save_stdout = sys.stdout
	sys.stdout = DummyFile()

	args = parser.parse_args(config.get_args())
	game = AmoebaGame(args)

	ok = game.goal_reached
	turns = game.turns
	ts = game.end_time - game.start_time

	# restore stdout
	sys.stdout = save_stdout

	return ok, turns, ts


# -----------------------------------------------------------------------------
# 	Script Entrypoint
# -----------------------------------------------------------------------------

if __name__ == "__main__":
	test_config = create_config(4, 5, 0.2, 1)

	ok, turns, ts = run(test_config)
	print("{} - {} turns in {:.2f} second(s)".format(
		"ok" if ok else "failed",
		turns,
		ts
	))