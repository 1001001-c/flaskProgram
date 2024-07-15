import math

def calculate_centrifuge(volume_in, mass_in, pcv, centrifuge_flush_volume, centrifuge_yield):
    volume_removed_by_pcv = volume_in * (pcv / 100)
    centrifuge_volume_out = (volume_in - volume_removed_by_pcv) + centrifuge_flush_volume
    centrifuge_mass_out = mass_in * (centrifuge_yield / 100)
    
    return {
        'volume_out': centrifuge_volume_out,
        'mass_out': centrifuge_mass_out,
        'volume_removed_by_pcv': volume_removed_by_pcv
    }
