import math

def calculate_depth_filtration(volume_in, mass_in, filter_library, filter_type, harvest_filter_loading_capacity, harvest_depth_filtration_yield, harvest_filter_wfi_flux_requirement, harvest_wfi_volume_per_filter_area, harvest_equilibration_volume_per_filter_area, harvest_chase_volume_per_filter_area, harvest_filter_process_flux_requirement):
    total_number_harvest_filter_required = math.ceil(volume_in / harvest_filter_loading_capacity)
    total_harvest_filter_area_installed = total_number_harvest_filter_required * filter_library[filter_type]['area']
    harvest_depth_filtration_mass_out = mass_in * (harvest_depth_filtration_yield / 100)
    harvest_depth_filtration_volume_out = (volume_in - (filter_library[filter_type]['discard_volume'] * total_harvest_filter_area_installed)) + (total_harvest_filter_area_installed * harvest_chase_volume_per_filter_area)
    number_harvest_filter_rack_required = math.ceil(total_number_harvest_filter_required / 10)

    max_flowrate = max(harvest_filter_process_flux_requirement, harvest_filter_wfi_flux_requirement)
    if max_flowrate <= 1200:
        pump_size = 'Quattraflow 1200 Pump'
    elif max_flowrate <= 2500:
        pump_size = 'Quattraflow 2500 Pump'
    else:
        pump_size = 'Quattraflow 4400 Pump'

    return {
        'volume_out': harvest_depth_filtration_volume_out,
        'mass_out': harvest_depth_filtration_mass_out,
        'total_number_harvest_filter_required': total_number_harvest_filter_required,
        'total_harvest_filter_area_installed': total_harvest_filter_area_installed,
        'number_harvest_filter_rack_required': number_harvest_filter_rack_required,
        'pump_size': pump_size
    }
