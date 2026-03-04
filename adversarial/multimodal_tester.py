#!/usr/bin/env python3
"""
Multi-Modal Adversarial Testing
Tests both text and image inputs for robustness.

🦀 13th Hour Multi-Modal Testing 🦀
"""

import base64
import hashlib
import json
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass
from enum import Enum
import random


class Modality(Enum):
    """Input/output modalities."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    MULTIMODAL = "multimodal"


@dataclass
class AdversarialImage:
    """Adversarial image perturbation description."""
    prompt: str
    perturbation_type: str
    strength: float
    target_class: Optional[str] = None
    metadata: Dict[str, Any] = None


class ImagePerturbationGenerator:
    """Generate adversarial image perturbations via prompt engineering."""

    PERTURBATION_TYPES = [
        "noise", "blur", "occlusion", "lighting", "rotation",
        "scaling", "compression", "watermark", "glitch", "style_transfer"
    ]

    NOISE_DESCRIPTIONS = [
        "heavy Gaussian noise",
        "salt and pepper noise",
        "perlin noise texture",
        "digital artifacts",
        "scan lines",
        "VHS distortion",
        "pixel sorting glitch"
    ]

    OCCLUSION_DESCRIPTIONS = [
        "partially obscured by {object}",
        "covered with {texture} pattern",
        "fragmented with {style} gaps",
        "mosaic censoring",
        "deep dream artifacts"
    ]

    OBJECTS = ["shadows", "hands", "objects", "text overlays", "geometric shapes"]
    TEXTURES = ["grid", "hexagonal", "noise", "organic", "crystalline"]
    STYLES = ["brutalist", "organic", "geometric", "chaotic", "minimal"]

    def __init__(self, seed: Optional[int] = None):
        if seed:
            random.seed(seed)

    def generate_perturbation(self, base_prompt: str, 
                             target_modality: str = "vision") -> AdversarialImage:
        """Generate adversarial image description."""

        perturbation_type = random.choice(self.PERTURBATION_TYPES)
        strength = random.uniform(0.1, 0.9)

        if perturbation_type == "noise":
            noise_desc = random.choice(self.NOISE_DESCRIPTIONS)
            prompt = f"{base_prompt}, with {noise_desc}, quality degraded"

        elif perturbation_type == "occlusion":
            template = random.choice(self.OCCLUSION_DESCRIPTIONS)
            occlusion = template.format(
                object=random.choice(self.OBJECTS),
                texture=random.choice(self.TEXTURES),
                style=random.choice(self.STYLES)
            )
            prompt = f"{base_prompt}, {occlusion}"

        elif perturbation_type == "glitch":
            glitch_types = ["RGB shift", "pixel sorting", "data bending", "scan line corruption"]
            prompt = f"{base_prompt}, {random.choice(glitch_types)} artifacts, corrupted data"

        elif perturbation_type == "lighting":
            lighting = ["extreme backlight", "harsh shadows", "overexposed", "underexposed", "unnatural colors"]
            prompt = f"{base_prompt}, {random.choice(lighting)}, poor lighting conditions"

        elif perturbation_type == "style_transfer":
            styles = ["oil painting", "watercolor", "sketch", "3D render", "pixel art", "surrealist"]
            prompt = f"{base_prompt}, rendered as {random.choice(styles)}, stylized"

        else:
            prompt = f"{base_prompt}, {perturbation_type} applied, quality affected"

        return AdversarialImage(
            prompt=prompt,
            perturbation_type=perturbation_type,
            strength=strength,
            metadata={
                "base_prompt": base_prompt,
                "target_modality": target_modality,
                "severity": "high" if strength > 0.7 else "medium" if strength > 0.4 else "low"
            }
        )

    def generate_universal_perturbation(self, target_classes: List[str]) -> AdversarialImage:
        """Generate universal adversarial perturbation prompt."""

        # Universal perturbations work across multiple classes
        patterns = [
            "high frequency noise pattern",
            "adversarial patch texture",
            "optimized noise texture",
            "class-agnostic perturbation"
        ]

        return AdversarialImage(
            prompt=f"Image with {random.choice(patterns)}, designed to confuse classifiers",
            perturbation_type="universal",
            strength=0.8,
            target_class="universal",
            metadata={
                "target_classes": target_classes,
                "attack_type": "universal_perturbation"
            }
        )


class MultiModalTester:
    """Test multi-modal model robustness."""

    def __init__(self, 
                 text_model: Callable,
                 image_model: Optional[Callable] = None,
                 multimodal_model: Optional[Callable] = None):
        """
        Initialize multi-modal tester.

        Args:
            text_model: Function for text-only inference
            image_model: Function for image-only inference
            multimodal_model: Function for combined text+image inference
        """
        self.text_model = text_model
        self.image_model = image_model
        self.multimodal_model = multimodal_model
        self.image_gen = ImagePerturbationGenerator()
        self.results: List[Dict] = []

    def test_text_image_consistency(self, 
                                   text_description: str,
                                   image_prompt: str,
                                   num_perturbations: int = 5) -> Dict:
        """Test if model treats text and image descriptions consistently."""

        # Get text prediction
        text_result = self.text_model(text_description)

        # Get image predictions with perturbations
        image_results = []
        for _ in range(num_perturbations):
            perturbed = self.image_gen.generate_perturbation(image_prompt)
            if self.image_model:
                result = self.image_model(perturbed.prompt)
                image_results.append({
                    "perturbation": perturbed.perturbation_type,
                    "strength": perturbed.strength,
                    "prediction": result
                })

        # Check consistency
        if self.multimodal_model:
            combined = self.multimodal_model({
                "text": text_description,
                "image": image_prompt
            })
        else:
            combined = None

        return {
            "text_prediction": text_result,
            "image_predictions": image_results,
            "combined_prediction": combined,
            "consistency_score": self._calculate_consistency(
                text_result, image_results, combined
            )
        }

    def test_cross_modal_attack(self, 
                               clean_text: str,
                               adversarial_image_desc: str) -> Dict:
        """Test if adversarial image affects text understanding."""

        # Clean baseline
        clean_result = self.multimodal_model({
            "text": clean_text,
            "image": "clean image of person"
        }) if self.multimodal_model else None

        # With adversarial image
        adversarial_result = self.multimodal_model({
            "text": clean_text,
            "image": adversarial_image_desc
        }) if self.multimodal_model else None

        # Check if image perturbation changed text understanding
        behavior_change = (
            clean_result != adversarial_result 
            if clean_result and adversarial_result 
            else False
        )

        return {
            "clean_result": clean_result,
            "adversarial_result": adversarial_result,
            "behavior_changed": behavior_change,
            "attack_successful": behavior_change
        }

    def test_modality_confusion(self, 
                               text: str,
                               image_desc: str,
                               swap_prob: float = 0.5) -> Dict:
        """Test if model confuses modalities when inputs are swapped."""

        # Normal order
        normal = self.multimodal_model({
            "text": text,
            "image": image_desc
        }) if self.multimodal_model else None

        # Swapped (text as image, image as text)
        # This tests if model properly handles modality tags
        swapped = self.multimodal_model({
            "text": image_desc,  # Image description as text
            "image": text        # Text as image description
        }) if self.multimodal_model else None

        # Should fail gracefully or detect mismatch
        return {
            "normal_order": normal,
            "swapped_order": swapped,
            "properly_handled": normal != swapped or swapped is None
        }

    def _calculate_consistency(self, text_pred, image_preds, combined_pred) -> float:
        """Calculate consistency score across modalities."""
        if not image_preds:
            return 1.0

        # Check if text matches image predictions
        text_class = text_pred.get('prediction') if isinstance(text_pred, dict) else text_pred

        matches = sum(
            1 for img in image_preds
            if img['prediction'].get('prediction') == text_class
        )

        return matches / len(image_preds)


class AudioAdversarialGenerator:
    """Generate adversarial audio perturbations."""

    PERTURBATIONS = [
        "white_noise_overlay",
        "background_chatter",
        "acoustic_echo",
        "clipping_distortion",
        "sample_rate_reduction",
        "mp3_compression_artifacts",
        "phase_shift",
        "frequency_filtering",
        "temporal_stretching",
        "adversarial_whisper"
    ]

    def generate_perturbation(self, base_audio_desc: str) -> Dict:
        """Generate adversarial audio description."""

        perturbation = random.choice(self.PERTURBATIONS)
        strength = random.uniform(0.1, 0.9)

        descriptions = {
            "white_noise_overlay": f"{base_audio_desc} with heavy white noise",
            "background_chatter": f"{base_audio_desc} with background conversations",
            "acoustic_echo": f"{base_audio_desc} with echo/reverb",
            "clipping_distortion": f"{base_audio_desc} with audio clipping",
            "sample_rate_reduction": f"{base_audio_desc} low quality, 8kHz sample rate",
            "mp3_compression_artifacts": f"{base_audio_desc} with compression artifacts",
            "phase_shift": f"{base_audio_desc} with phase issues",
            "frequency_filtering": f"{base_audio_desc} with muffled frequencies",
            "temporal_stretching": f"{base_audio_desc} time-stretched",
            "adversarial_whisper": f"{base_audio_desc} with subliminal whisper overlay"
        }

        return {
            "description": descriptions.get(perturbation, base_audio_desc),
            "perturbation_type": perturbation,
            "strength": strength,
            "target": "speech_recognition" if "voice" in base_audio_desc else "audio_classification"
        }


if __name__ == "__main__":
    # Demo
    print("🦀 Multi-Modal Adversarial Testing Demo 🦀\n")

    img_gen = ImagePerturbationGenerator(seed=13)

    base = "Professional headshot of a software engineer"

    print("Image Perturbations:")
    for i in range(5):
        pert = img_gen.generate_perturbation(base)
        print(f"  {i+1}. {pert.perturbation_type} (strength: {pert.strength:.2f})")
        print(f"     Prompt: {pert.prompt[:80]}...")
