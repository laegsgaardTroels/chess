# import pytest
# from chess import agent
# from chess.__main__ import simulate
# from chess._constants import WHITE, BLACK, STARTING_BOARD, STATE_DTYPE, ACTION_DTYPE
# from chess import _utils
#
#
# @pytest.mark.parametrize(
#     "white_player,black_player,seed",
#     [
#         (agent.RandomAgent(color=WHITE), agent.RandomAgent(color=BLACK), 0),
#         (agent.RandomAgent(color=WHITE), agent.AlphaBetaAgent(color=BLACK, depth=1), 0),
#         (
#             agent.AlphaBetaAgent(color=WHITE, depth=1),
#             agent.AlphaBetaAgent(color=BLACK, depth=1),
#             0,
#         ),
#     ],
# )
# def test_simulate_random_agent_vs_random_agent(white_player, black_player, seed):
#     state_log, action_log = simulate(
#         color=WHITE,
#         board=STARTING_BOARD,
#         white_player=white_player,
#         black_player=black_player,
#         verbose=False,
#         seed=seed,
#         max_rounds=10,
#     )
#     assert state_log.dtype == STATE_DTYPE
#     assert action_log.dtype == ACTION_DTYPE
#     assert len(state_log) == 10
#     assert len(state_log) == len(action_log)
#
#
# def test_alpha_beta_agent():
#     state = _utils.init_state()
#     a = agent.AlphaBetaAgent(color=WHITE, depth=1)
#     assert a.state_value(state) == 0
#
#     a = agent.AlphaBetaAgent(color=BLACK, depth=1)
#     assert a.state_value(state) == 0
