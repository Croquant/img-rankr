from time import perf_counter

import dhash
from django.core.management.base import BaseCommand

from image.models import Image


class Command(BaseCommand):
    args = "<start end>"
    help = "Update Torikumi results"

    def handle(self, *args, **options):
        start_time = perf_counter()
        images = Image.objects.all()

        closest_pairs = []  # Initialize an empty list for closest pairs

        for img in images:
            others = Image.objects.exclude(id=img.id)

            for other in others:
                diff = dhash.get_num_bits_different(
                    int(img.file_hash, 16), int(other.file_hash, 16)
                )

                # Check if the pair is a duplicate (reversed order)
                reversed_pair = (other.file_url, img.file_url, diff)
                if reversed_pair not in closest_pairs:
                    # Add the pair to the list if it's one of the top 10 closest
                    if len(closest_pairs) < 10:
                        closest_pairs.append(
                            (img.file_url, other.file_url, diff)
                        )
                    else:
                        # Replace the pair with the highest difference if the current pair is closer
                        max_diff_pair = max(closest_pairs, key=lambda x: x[2])
                        if diff < max_diff_pair[2]:
                            closest_pairs.remove(max_diff_pair)
                            closest_pairs.append(
                                (img.file_url, other.file_url, diff)
                            )

        # Sort the pairs by difference value (ascending order)
        closest_pairs.sort(key=lambda x: x[2])

        # Print the top 10 closest pairs
        for pair in closest_pairs:
            print(f"Pair: {pair[0]} - {pair[1]}, Difference: {pair[2]}")

        elapsed_time = perf_counter() - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")
