## Asset Catalog for v0.2.0

### Assets

```
.
├── Policies
│   └── LiverScan
│       ├── GR00TN1_Cosmos_Rel
│       │   ├── config.json
│       │   ├── experiment_cfg
│       │   │   └── metadata.json
│       │   ├── model-00001-of-00002.safetensors
│       │   ├── model-00002-of-00002.safetensors
│       │   ├── model.safetensors.index.json
│       │   ├── optimizer.pt
│       │   ├── rng_state_0.pth
│       │   ├── rng_state_1.pth
│       │   ├── rng_state_2.pth
│       │   ├── rng_state_3.pth
│       │   ├── scheduler.pt
│       │   └── trainer_state.json
│       └── Pi0_Cosmos_Rel
│           ├── assets
│           │   └── i4h
│           │       └── sim_liver_scan
│           │           └── norm_stats.json
│           └── params
│               ├── d
│               │   └── c3cdb11d58976c226289a88877d79df2
│               ├── manifest.ocdbt
│               ├── _METADATA
│               ├── ocdbt.process_0
│               │   ├── d
│               │   │   ├── 03eabde80a89e810a0afc1abcf5c7848
│               │   │   ├── 05fbcf2cfc03e3088c40e5cca64337ff
│               │   │   ├── 1de4850609ecde45a12e8b7f6307d1c5
│               │   │   ├── 205cfc13124e02e4a89c8b75434254f5
│               │   │   ├── 2360a4fcd039e9b7c988e9371516e154
│               │   │   ├── 41e47400759333602c0a03c2aac86fb8
│               │   │   ├── 59bfe2f920dc04f52a558077604b989e
│               │   │   ├── 764259551469e1207ecb84f0a97f2f13
│               │   │   ├── 7c6cbfa3d7dde39b19632bc491d19aab
│               │   │   ├── 7ec24389d31b243062bc76eaa35b8230
│               │   │   ├── 819151e609606ddf26a1a44fd4ccf2f1
│               │   │   ├── 8ae08870d657d1ffc465b832d2483d43
│               │   │   ├── a1542eea92e381fe227482d6b39a896f
│               │   │   ├── a97f9d625615b4db4de8d3ab3376190c
│               │   │   ├── dd12d1bc476a51cd183ce995493a2342
│               │   │   ├── df389e0a1e2615e5cdc0026d6ea348fa
│               │   │   ├── e5098cbce201e826410f8e5c6738a801
│               │   │   ├── eacbd5b61c081c47b986298b8a88902e
│               │   │   ├── f5df773fd80cf44a1990ea53735ce9ab
│               │   │   └── fed6f6f223ea75b1069502cd40028631
│               │   └── manifest.ocdbt
│               └── _sharding
├── Props
│   ├── ABDPhantom
│   │   ├── Organs
│   │   │   ├── Back_muscles.mtl
│   │   │   ├── Back_muscles.obj
│   │   │   ├── Bone.mtl
│   │   │   ├── Bone.obj
│   │   │   ├── Colon.mtl
│   │   │   ├── Colon.obj
│   │   │   ├── Gallbladder.mtl
│   │   │   ├── Gallbladder.obj
│   │   │   ├── Heart.mtl
│   │   │   ├── Heart.obj
│   │   │   ├── Kidney.mtl
│   │   │   ├── Kidney.obj
│   │   │   ├── Liver.mtl
│   │   │   ├── Liver.obj
│   │   │   ├── Lungs.mtl
│   │   │   ├── Lungs.obj
│   │   │   ├── Pancreas.mtl
│   │   │   ├── Pancreas.obj
│   │   │   ├── Skin.mtl
│   │   │   ├── Skin.obj
│   │   │   ├── Small_bowel.mtl
│   │   │   ├── Small_bowel.obj
│   │   │   ├── Spleen.mtl
│   │   │   ├── Spleen.obj
│   │   │   ├── Stomach.mtl
│   │   │   ├── Stomach.obj
│   │   │   ├── Tumor1.mtl
│   │   │   ├── Tumor1.obj
│   │   │   ├── Tumor2.mtl
│   │   │   ├── Tumor2.obj
│   │   │   ├── Vessels.mtl
│   │   │   └── Vessels.obj
│   │   ├── phantom.usda
│   │   └── SubUSDs
│   │       └── textures
│   │           └── sample_texture0.png
│   ├── Board
│   │   ├── board.usd
│   │   └── parts
│   │       ├── pegboard_base.usd
│   │       ├── pegboard.usd
│   │       ├── peg.usd
│   │       └── screw_M3x10.usd
│   ├── ClariusUltrasoundProbe
│   │   └── fixture.usda
│   ├── D405
│   │   └── D405_blend.usd
│   ├── Organs
│   │   ├── materials
│   │   │   ├── human_skin_normal_detail.jpg
│   │   │   ├── operating_room
│   │   │   │   ├── Base
│   │   │   │   │   ├── Architecture
│   │   │   │   │   │   ├── Ceiling_Tiles
│   │   │   │   │   │   │   ├── Ceiling_Tiles_BaseColor.png
│   │   │   │   │   │   │   ├── Ceiling_Tiles_Normal.png
│   │   │   │   │   │   │   └── Ceiling_Tiles_ORM.png
│   │   │   │   │   │   └── Ceiling_Tiles.mdl
│   │   │   │   │   ├── Emissives
│   │   │   │   │   │   └── Light_5500K.mdl
│   │   │   │   │   ├── Glass
│   │   │   │   │   │   ├── Clear_Glass.mdl
│   │   │   │   │   │   ├── Glazed_Glass.mdl
│   │   │   │   │   │   └── Mirror.mdl
│   │   │   │   │   ├── Masonry
│   │   │   │   │   │   ├── Stucco
│   │   │   │   │   │   │   ├── Stucco_BaseColor.png
│   │   │   │   │   │   │   ├── Stucco_Normal.png
│   │   │   │   │   │   │   └── Stucco_ORM.png
│   │   │   │   │   │   └── Stucco.mdl
│   │   │   │   │   ├── Metals
│   │   │   │   │   │   ├── Aluminum_Anodized
│   │   │   │   │   │   │   ├── Aluminum_Anodized_BaseColor.png
│   │   │   │   │   │   │   ├── Aluminum_Anodized_Normal.png
│   │   │   │   │   │   │   └── Aluminum_Anodized_ORM.png
│   │   │   │   │   │   ├── Aluminum_Anodized_Blue.mdl
│   │   │   │   │   │   ├── Aluminum_Polished
│   │   │   │   │   │   │   ├── Aluminum_Polished_BaseColor.png
│   │   │   │   │   │   │   ├── Aluminum_Polished_Normal.png
│   │   │   │   │   │   │   └── Aluminum_Polished_ORM.png
│   │   │   │   │   │   └── Aluminum_Polished.mdl
│   │   │   │   │   ├── Miscellaneous
│   │   │   │   │   │   ├── Paint_Gloss_Finish
│   │   │   │   │   │   │   ├── Paint_Gloss_Finish_BaseColor.png
│   │   │   │   │   │   │   ├── Paint_Gloss_Finish_N.png
│   │   │   │   │   │   │   └── Paint_Gloss_Finish_ORM.png
│   │   │   │   │   │   └── Paint_Gloss_Finish.mdl
│   │   │   │   │   ├── Plastics
│   │   │   │   │   │   ├── Plastic_Clear.mdl
│   │   │   │   │   │   └── Plastic.mdl
│   │   │   │   │   ├── Stone
│   │   │   │   │   │   ├── Ceramic_Smooth_Fired
│   │   │   │   │   │   │   ├── Ceramic_Smooth_Fired_BaseColor.png
│   │   │   │   │   │   │   ├── Ceramic_Smooth_Fired_N.png
│   │   │   │   │   │   │   └── Ceramic_Smooth_Fired_ORM.png
│   │   │   │   │   │   ├── Ceramic_Smooth_Fired.mdl
│   │   │   │   │   │   ├── Terrazzo
│   │   │   │   │   │   │   ├── Terrazzo_BaseColor.png
│   │   │   │   │   │   │   ├── Terrazzo_N.png
│   │   │   │   │   │   │   └── Terrazzo_ORM.png
│   │   │   │   │   │   └── Terrazzo.mdl
│   │   │   │   │   ├── Templates
│   │   │   │   │   │   ├── GlassUtils.mdl
│   │   │   │   │   │   └── GlassWithVolume.mdl
│   │   │   │   │   └── Wood
│   │   │   │   │       ├── Ash
│   │   │   │   │       │   ├── Ash_BaseColor.png
│   │   │   │   │       │   ├── Ash_Normal.png
│   │   │   │   │       │   └── Ash_ORM.png
│   │   │   │   │       └── Ash.mdl
│   │   │   │   └── Metal
│   │   │   │       ├── Aluminum_Brushed.mdl
│   │   │   │       └── textures
│   │   │   │           ├── brushed_metal_linear_norm.jpg
│   │   │   │           └── brushed_metal_linear_R_rough_G_scratchvar_B_impurities.jpg
│   │   │   ├── operating_table
│   │   │   │   ├── Table_baseColor.jpg
│   │   │   │   ├── Table_metallicRoughness_metal.jpg
│   │   │   │   ├── Table_metallicRoughness_rough.jpg
│   │   │   │   └── Table_normal.jpg
│   │   │   └── organs
│   │   │       ├── Back_muscles
│   │   │       │   ├── Back_muscles_topo_blender_ambientocclusion.1001.png
│   │   │       │   ├── Back_muscles_topo_blender_curvature.1001.png
│   │   │       │   ├── Back_muscles_topo_blender_diffuseReflectionColor.1001.png
│   │   │       │   ├── Back_muscles_topo_blender_geometryDisplacement.1001.png
│   │   │       │   ├── Back_muscles_topo_blender_geometryNormal.1001.png
│   │   │       │   ├── Back_muscles_topo_blender_specularReflectionRoughness.1001.png
│   │   │       │   └── Back_muscles_topo_blender_subsurfaceWeight.1001.png
│   │   │       ├── Body
│   │   │       │   ├── Body_topo_ambientocclusion.1001.png
│   │   │       │   ├── Body_topo_curvature.1001.png
│   │   │       │   ├── Body_topo_diffuseReflectionColor.1001.png
│   │   │       │   ├── Body_topo_geometryDisplacement.1001.png
│   │   │       │   ├── Body_topo_geometryNormal.1001.png
│   │   │       │   ├── Body_topo_specularReflectionRoughness.1001.png
│   │   │       │   └── Body_topo_subsurfaceWeight.1001.png
│   │   │       ├── Colon
│   │   │       │   ├── Colon_topo_blender_ambientocclusion.1001.png
│   │   │       │   ├── Colon_topo_blender_curvature.1001.png
│   │   │       │   ├── Colon_topo_blender_diffuseReflectionColor.1001.png
│   │   │       │   ├── Colon_topo_blender_geometryDisplacement.1001.png
│   │   │       │   ├── Colon_topo_blender_geometryNormal.1001.png
│   │   │       │   ├── Colon_topo_blender_specularReflectionRoughness.1001.png
│   │   │       │   └── Colon_topo_blender_subsurfaceWeight.1001.png
│   │   │       ├── Gallbladder
│   │   │       │   ├── Gallbladder_topo_blender_ambientocclusion.1001.png
│   │   │       │   ├── Gallbladder_topo_blender_curvature.1001.png
│   │   │       │   ├── Gallbladder_topo_blender_diffuseReflectionColor.1001.png
│   │   │       │   ├── Gallbladder_topo_blender_geometryDisplacement.1001.png
│   │   │       │   ├── Gallbladder_topo_blender_geometryNormal.1001.png
│   │   │       │   ├── Gallbladder_topo_blender_specularReflectionRoughness.1001.png
│   │   │       │   └── Gallbladder_topo_blender_subsurfaceWeight.1001.png
│   │   │       ├── Heart
│   │   │       │   ├── Heart_topo_blender_ambientocclusion.1001.png
│   │   │       │   ├── Heart_topo_blender_curvature.1001.png
│   │   │       │   ├── Heart_topo_blender_diffuseReflectionColor.1001.png
│   │   │       │   ├── Heart_topo_blender_geometryDisplacement.1001.png
│   │   │       │   ├── Heart_topo_blender_geometryNormal.1001.png
│   │   │       │   ├── Heart_topo_blender_specularReflectionRoughness.1001.png
│   │   │       │   └── Heart_topo_blender_subsurfaceWeight.1001.png
│   │   │       ├── Hips
│   │   │       │   ├── Hips_topo_blender_ambientocclusion.1001.png
│   │   │       │   ├── Hips_topo_blender_curvature.1001.png
│   │   │       │   ├── Hips_topo_blender_diffuseReflectionColor.1001.png
│   │   │       │   ├── Hips_topo_blender_geometryDisplacement.1001.png
│   │   │       │   ├── Hips_topo_blender_geometryNormal.1001.png
│   │   │       │   ├── Hips_topo_blender_specularReflectionRoughness.1001.png
│   │   │       │   └── Hips_topo_blender_subsurfaceWeight.1001.png
│   │   │       ├── Kidneys
│   │   │       │   ├── Kidney_topo_blender_ambientocclusion.1001.png
│   │   │       │   ├── Kidney_topo_blender_curvature.1001.png
│   │   │       │   ├── Kidney_topo_blender_diffuseReflectionColor.1001.png
│   │   │       │   ├── Kidney_topo_blender_geometryDisplacement.1001.png
│   │   │       │   ├── Kidney_topo_blender_geometryNormal.1001.png
│   │   │       │   ├── Kidney_topo_blender_specularReflectionRoughness.1001.png
│   │   │       │   └── Kidney_topo_blender_subsurfaceWeight.1001.png
│   │   │       ├── Liver
│   │   │       │   ├── Liver_topo_blender_ambientocclusion.1001.png
│   │   │       │   ├── Liver_topo_blender_curvature.1001.png
│   │   │       │   ├── Liver_topo_blender_diffuseReflectionColor.1001.png
│   │   │       │   ├── Liver_topo_blender_geometryDisplacement.1001.png
│   │   │       │   ├── Liver_topo_blender_geometryNormal.1001.png
│   │   │       │   ├── Liver_topo_blender_specularReflectionRoughness.1001.png
│   │   │       │   └── Liver_topo_blender_subsurfaceWeight.1001.png
│   │   │       ├── Lungs
│   │   │       │   ├── Lungs_topo_blender_ambientocclusion.1001.png
│   │   │       │   ├── Lungs_topo_blender_curvature.1001.png
│   │   │       │   ├── Lungs_topo_blender_diffuseReflectionColor.1001.png
│   │   │       │   ├── Lungs_topo_blender_geometryDisplacement.1001.png
│   │   │       │   ├── Lungs_topo_blender_geometryNormal.1001.png
│   │   │       │   ├── Lungs_topo_blender_specularReflectionRoughness.1001.png
│   │   │       │   └── Lungs_topo_blender_subsurfaceWeight.1001.png
│   │   │       ├── Pancreas
│   │   │       │   ├── Pancreas_topo_blender_ambientocclusion.1001.png
│   │   │       │   ├── Pancreas_topo_blender_curvature.1001.png
│   │   │       │   ├── Pancreas_topo_blender_diffuseReflectionColor.1001.png
│   │   │       │   ├── Pancreas_topo_blender_geometryDisplacement.1001.png
│   │   │       │   ├── Pancreas_topo_blender_geometryNormal.1001.png
│   │   │       │   ├── Pancreas_topo_blender_specularReflectionRoughness.1001.png
│   │   │       │   └── Pancreas_topo_blender_subsurfaceWeight.1001.png
│   │   │       ├── Ribs
│   │   │       │   ├── Ribs_topo_blender_ambientocclusion.1001.png
│   │   │       │   ├── Ribs_topo_blender_curvature.1001.png
│   │   │       │   ├── Ribs_topo_blender_diffuseReflectionColor.1001.png
│   │   │       │   ├── Ribs_topo_blender_geometryDisplacement.1001.png
│   │   │       │   ├── Ribs_topo_blender_geometryNormal.1001.png
│   │   │       │   ├── Ribs_topo_blender_specularReflectionRoughness.1001.png
│   │   │       │   └── Ribs_topo_blender_subsurfaceWeight.1001.png
│   │   │       ├── Shoulders
│   │   │       │   ├── Shoulders_topo_blender_diffuseReflectionColor.1001.png
│   │   │       │   ├── Shoulders_topo_blender_geometryNormal.1001.png
│   │   │       │   ├── Shoulders_topo_blender_specularReflectionRoughness.1001.png
│   │   │       │   └── Shoulders_topo_blender_subsurfaceWeight.1001.png
│   │   │       ├── Small_bowel
│   │   │       │   ├── Small_bowel_topo_blender_ambientocclusion.1001.png
│   │   │       │   ├── Small_bowel_topo_blender_curvature.1001.png
│   │   │       │   ├── Small_bowel_topo_blender_diffuseReflectionColor.1001.png
│   │   │       │   ├── Small_bowel_topo_blender_geometryDisplacement.1001.png
│   │   │       │   ├── Small_bowel_topo_blender_geometryNormal.1001.png
│   │   │       │   ├── Small_bowel_topo_blender_specularReflectionRoughness.1001.png
│   │   │       │   └── Small_bowel_topo_blender_subsurfaceWeight.1001.png
│   │   │       ├── Spine
│   │   │       │   ├── Spine_topo_blender_ambientocclusion.1001.png
│   │   │       │   ├── Spine_topo_blender_curvature.1001.png
│   │   │       │   ├── Spine_topo_blender_diffuseReflectionColor.1001.png
│   │   │       │   ├── Spine_topo_blender_geometryDisplacement.1001.png
│   │   │       │   ├── Spine_topo_blender_geometryNormal.1001.png
│   │   │       │   ├── Spine_topo_blender_specularReflectionRoughness.1001.png
│   │   │       │   ├── Spine_topo_blender_subsurfaceWeight.1001.png
│   │   │       │   ├── Spine_topo_new_ambientocclusion.1001.png
│   │   │       │   ├── Spine_topo_new_curvature.1001.png
│   │   │       │   ├── Spine_topo_new_diffuseReflectionColor.1001.png
│   │   │       │   ├── Spine_topo_new_geometryDisplacement.1001.png
│   │   │       │   ├── Spine_topo_new_geometryNormal.1001.png
│   │   │       │   ├── Spine_topo_new_specularReflectionRoughness.1001.png
│   │   │       │   └── Spine_topo_new_subsurfaceWeight.1001.png
│   │   │       ├── Spleen
│   │   │       │   ├── Spleen_topo_blender_ambientocclusion.1001.png
│   │   │       │   ├── Spleen_topo_blender_curvature.1001.png
│   │   │       │   ├── Spleen_topo_blender_diffuseReflectionColor.1001.png
│   │   │       │   ├── Spleen_topo_blender_geometryDisplacement.1001.png
│   │   │       │   ├── Spleen_topo_blender_geometryNormal.1001.png
│   │   │       │   ├── Spleen_topo_blender_specularReflectionRoughness.1001.png
│   │   │       │   └── Spleen_topo_blender_subsurfaceWeight.1001.png
│   │   │       ├── Stomach
│   │   │       │   ├── Stomach_topo_blender_ambientocclusion.1001.png
│   │   │       │   ├── Stomach_topo_blender_curvature.1001.png
│   │   │       │   ├── Stomach_topo_blender_diffuseReflectionColor.1001.png
│   │   │       │   ├── Stomach_topo_blender_geometryDisplacement.1001.png
│   │   │       │   ├── Stomach_topo_blender_geometryNormal.1001.png
│   │   │       │   ├── Stomach_topo_blender_specularReflectionRoughness.1001.png
│   │   │       │   └── Stomach_topo_blender_subsurfaceWeight.1001.png
│   │   │       └── Veins
│   │   │           ├── Veins_topo_blender_ambientocclusion.1001.png
│   │   │           ├── Veins_topo_blender_curvature.1001.png
│   │   │           ├── Veins_topo_blender_diffuseReflectionColor.1001.png
│   │   │           ├── Veins_topo_blender_geometryDisplacement.1001.png
│   │   │           ├── Veins_topo_blender_geometryNormal.1001.png
│   │   │           ├── Veins_topo_blender_specularReflectionRoughness.1001.png
│   │   │           └── Veins_topo_blender_subsurfaceWeight.1001.png
│   │   ├── models
│   │   │   ├── operating_room
│   │   │   │   ├── ceiling_lamps
│   │   │   │   │   └── Over_GRP_CeilingLamps_merged.usd
│   │   │   │   └── room
│   │   │   │       ├── Over_GRP_Room_Additions_merged.usd
│   │   │   │       └── textures
│   │   │   │           ├── TexturesCom_WoodFine0058_30_seamless_M.png
│   │   │   │           ├── T_Floor_D.jpg
│   │   │   │           ├── T_Products_D.jpg
│   │   │   │           └── T_Wall_D.jpg
│   │   │   ├── operating_table
│   │   │   │   └── Operating_table.obj
│   │   │   └── organs
│   │   │       └── models_topo_blender.usdc
│   │   ├── organs.usd
│   │   └── shaders
│   │       ├── operating_table
│   │       │   └── table_shader.usd
│   │       └── organs
│   │           └── organ_shaders.usd
│   ├── PegBlock
│   │   └── block.usd
│   ├── SutureNeedle
│   │   ├── needle_sdf.usd
│   │   └── needle.usd
│   ├── SuturePad
│   │   └── suture_pad.usd
│   ├── Table
│   │   └── table.usd
│   ├── UltrasoundCameraFixture
│   │   ├── collect.mapping.json
│   │   └── fixture.usda
│   ├── VentionTable
│   │   └── table.usda
│   └── VentionTableWithBlackCover
│       ├── table
│       │   └── table_cover.usdc
│       └── table_with_cover.usd
├── Robots
│   ├── dVRK
│   │   ├── ECM
│   │   │   └── ecm.usd
│   │   └── PSM
│   │       └── psm.usd
│   ├── Franka
│   │   ├── Collected_fr3_assembly
│   │   │   └── fr3_assembly.usda
│   │   ├── Collected_panda_assembly
│   │   │   └── panda_assembly.usda
│   │   └── End_effector
│   │       ├── HD3C3 Endeffector.step
│   │       └── LICENSE
│   ├── MIRA
│   │   ├── mira-bipo-size-experiment-smoothing.usd
│   │   ├── suture-needle.usd
│   │   └── textures
│   │       └── plastic_normal.jpg
│   └── STAR
│       └── star.usd
└── Test
    └── basic.usda

94 directories, 282 files
```
