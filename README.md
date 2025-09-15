# Isaac for Healthcare - Asset Catalog

The Isaac for Healthcare (i4h) asset catalog is a collection of assets that are used to create the i4h simulation environment.

## Asset Categories

The i4h asset catalog contains several categories of assets that are essential for creating realistic healthcare simulations:

### Pre-trained Models
- **Medical Imaging Models**: Deep learning models trained for medical image analysis, segmentation, and diagnosis
- **Surgical Planning Models**: AI models for surgical procedure planning and optimization
- **Patient-specific Models**: Models trained on patient data for personalized healthcare applications

### Simulation-Ready Robots
- **Surgical Robots**: Detailed 3D models of surgical robotic systems with accurate kinematics and dynamics
- **Medical Assist Robots**: Models of robots used for patient assistance and care
- **Lab Automation Robots**: Models of robots used in laboratory settings

### Anatomical Models
- **Standard Anatomy**: High-fidelity 3D models of human anatomy for general simulation
- **Pathological Models**: Models representing various disease states and conditions
- **BYO (Bring Your Own) Anatomy**: Support for importing custom anatomical models with proper documentation and validation guidelines

### Visual Assets
- **Medical Equipment**: 3D models of medical devices and equipment
- **Hospital Environment**: Models of hospital rooms, operating theaters, and medical facilities
- **Materials and Textures**: High-quality textures and materials for realistic rendering

### Configuration Files
- **Simulation Parameters**: Configuration files for physics, rendering, and simulation settings
- **Workflow Templates**: Pre-configured workflow templates for common medical procedures
- **Environment Setups**: Configuration files for different simulation environments

## Asset Documentation
Each asset category includes detailed documentation, usage guidelines, and compatibility information to ensure proper integration into the i4h simulation environment.

## Version Information
The asset catalog follows the Isaac Lab asset structure. You can find the asset for each version in the corresponding folders.

### Version 0.3.0

- Added assets for the new SO-ARM starter workflow.
- Added hospital environment assets.
- Moved the policy models to Hugging Face `nvidia` organization.

Catalog: [v0.3.0](./docs/catalog_v0.3.0.md)

### Version 0.2.0
Contains all assets from Version 0.1.0 plus:
- Pre-trained models for liver scanning:
  - GR00TN1
  - GR00TN1_Cosmos
  - Pi0 model with Cosmos
- Mira Surgical Robot

Catalog: [v0.2.0](./docs/catalog_v0.2.0.md)

### Version 0.1.0
Contains the initial release of the asset catalog with:
- Basic anatomical models
- Standard medical equipment
- Hospital environment assets
- Franka Robot Assets
- Pi0 models including:
  - Liver scan policies and configurations
  - Model weights and training states
  - Normalization statistics
  - Parameter manifests and metadata

Catalog: [v0.1.0](./docs/catalog_v0.1.0.md)

## Asset Helper Tool
You can also use the `i4h_asset_helper` package to get the download links for the assets. For more details, please refer to [I4H Assets Catalog Helper](./docs/catalog_helper.md).
