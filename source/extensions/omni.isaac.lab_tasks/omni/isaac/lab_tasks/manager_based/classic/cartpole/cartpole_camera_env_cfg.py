# Copyright (c) 2022-2024, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import omni.isaac.lab.sim as sim_utils
from omni.isaac.lab.envs.mdp.observations import grab_images
from omni.isaac.lab.managers import ObservationGroupCfg as ObsGroup
from omni.isaac.lab.managers import ObservationTermCfg as ObsTerm
from omni.isaac.lab.managers import SceneEntityCfg
from omni.isaac.lab.sensors import TiledCameraCfg
from omni.isaac.lab.utils import configclass

from omni.isaac.lab_tasks.manager_based.classic.cartpole.cartpole_env_cfg import CartpoleEnvCfg, CartpoleSceneCfg

##
# Scene definition
##


@configclass
class CartpoleRGBCameraSceneCfg(CartpoleSceneCfg):
    tiled_camera: TiledCameraCfg = TiledCameraCfg(
        prim_path="{ENV_REGEX_NS}/Camera",
        offset=TiledCameraCfg.OffsetCfg(pos=(-7.0, 0.0, 3.0), rot=(0.9945, 0.0, 0.1045, 0.0), convention="world"),
        data_types=["rgb"],
        spawn=sim_utils.PinholeCameraCfg(
            focal_length=24.0, focus_distance=400.0, horizontal_aperture=20.955, clipping_range=(0.1, 20.0)
        ),
        width=80,
        height=80,
    )


@configclass
class CartpoleDepthCameraSceneCfg(CartpoleSceneCfg):
    tiled_camera: TiledCameraCfg = TiledCameraCfg(
        prim_path="{ENV_REGEX_NS}/Camera",
        offset=TiledCameraCfg.OffsetCfg(pos=(-7.0, 0.0, 3.0), rot=(0.9945, 0.0, 0.1045, 0.0), convention="world"),
        data_types=["distance_to_camera"],
        spawn=sim_utils.PinholeCameraCfg(
            focal_length=24.0, focus_distance=400.0, horizontal_aperture=20.955, clipping_range=(0.1, 20.0)
        ),
        width=80,
        height=80,
    )


@configclass
class RGBObservationsCfg:
    """Observation specifications for the MDP."""

    @configclass
    class RGBCameraPolicyCfg(ObsGroup):
        """Observations for policy group."""

        image = ObsTerm(func=grab_images, params={"sensor_cfg": SceneEntityCfg("tiled_camera"), "data_type": "rgb"})

        def __post_init__(self) -> None:
            self.enable_corruption = False
            self.concatenate_terms = True

    policy: ObsGroup = RGBCameraPolicyCfg()


@configclass
class DepthObservationsCfg:
    @configclass
    class DepthCameraPolicyCfg(RGBObservationsCfg.RGBCameraPolicyCfg):
        image = ObsTerm(
            func=grab_images, params={"sensor_cfg": SceneEntityCfg("tiled_camera"), "data_type": "distance_to_camera"}
        )

    policy: ObsGroup = DepthCameraPolicyCfg()


@configclass
class CartpoleRGBCameraEnvCfg(CartpoleEnvCfg):
    scene: CartpoleSceneCfg = CartpoleRGBCameraSceneCfg(num_envs=1024, env_spacing=20)
    observations = RGBObservationsCfg()


@configclass
class CartpoleDepthCameraEnvCfg(CartpoleEnvCfg):
    scene: CartpoleSceneCfg = CartpoleDepthCameraSceneCfg(num_envs=1024, env_spacing=20)
    observations = DepthObservationsCfg()
