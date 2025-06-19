from device_service import DeviceRepository, DeviceService
from hub_service import HubService, HubRepository
from dwelling_service import DwellingService, DwellingRepo
from pairing_repository import PairingRepository

pairing_repository = PairingRepository()

device_service = DeviceService(DeviceRepository(), pairing_repository)
hub_service = HubService(HubRepository(), pairing_repository, device_service)
dwelling_service = DwellingService(DwellingRepo())


if __name__ == "__main__":
    print("=== IoT Device Tracking System Demo ===\n")

    print("Creating devices...")
    switch = device_service.create("switch")
    print(f"Created Switch ID: {switch.get_id()}")
    dimmer = device_service.create("dimmer")
    print(f"Created Dimmer ID: {dimmer.get_id()}")
    lock = device_service.create("lock")
    print(f"Created Lock ID: {lock.get_id()}")
    thermostat = device_service.create("thermostat")
    print(f"Created Thermostat ID: {thermostat.get_id()}")

    print("\nListing all devices...")
    devices = device_service.list_devices()
    for device in devices:
        print(f"{device._type.value}: {device.get_id()}")

    print("\nModifying device states...")
    device_service.modify(switch.get_id(), state="on")
    print("Turned on switch")
    device_service.modify(dimmer.get_id(), brightness=75)
    print("Set dimmer brightness to 75")
    device_service.modify(lock.get_id(), pin_code="1234", state="unlocked")
    print("Set lock pin and unlocked")
    device_service.modify(thermostat.get_id(), temperature=25)
    print("Set thermostat to 25")

    print("\nGetting device states")
    print(f"Switch info: {device_service.info(switch.get_id())}")
    print(f"Dimmer info: {device_service.info(dimmer.get_id())}")
    print(f"Lock info: {device_service.info(lock.get_id())}")
    print(f"Thermostat info: {device_service.info(thermostat.get_id())}")

    print("\nCreating hubs...")
    hub1 = hub_service.create()
    print(f"Created Hub 1 ID: {hub1.get_id()}")
    hub2 = hub_service.create()
    print(f"Created Hub 2 ID: {hub2.get_id()}")

    print("\nCreating dwellings...")
    dwelling1 = dwelling_service.create_dwelling()
    print(f"Created Dwelling 1 ID: {dwelling1.get_id()}")
    dwelling2 = dwelling_service.create_dwelling()
    print(f"Created Dwelling 2 ID: {dwelling2.get_id()}")

    print("\nListing all dwellings...")
    dwellings = dwelling_service.list_dwellings()
    for dwelling in dwellings:
        print(f"Occupied={dwelling._occupied}, id={dwelling.get_id()}")

    dwelling_service.occupied(dwelling1.get_id())
    print(f"\nSet dwelling {dwelling1.get_id()} as occupied")
    dwelling_service.occupied(dwelling2.get_id())
    print(f"Set dwelling {dwelling2.get_id()} as vacant")

    print("\nInstalling hubs in dwellings...")
    dwelling_service.install_hub(dwelling1.get_id(), hub1.get_id())
    print(f"Installed hub:{hub1.get_id()} in dwelling {dwelling1.get_id()}")
    dwelling_service.install_hub(dwelling2.get_id(), hub2.get_id())
    print(f"Installed hub:{hub2.get_id()} in dwelling {dwelling2.get_id()}")

    print("\nPairing devices to hubs...")
    hub_service.pair_device_to_hub(hub1.get_id(), switch.get_id())
    hub_service.pair_device_to_hub(hub1.get_id(), dimmer.get_id())
    print(f"Paired devices({switch.get_id()},{dimmer.get_id()}) to hub:{hub1.get_id()}")
    print(f"Listing devices paired to Hub: {hub1.get_id()}")
    for device in hub_service.list_devices(hub1.get_id()):
        print(f"Device info:{device.get_info()}")

    hub_service.pair_device_to_hub(hub2.get_id(), lock.get_id())
    hub_service.pair_device_to_hub(hub2.get_id(), thermostat.get_id())
    print(
        f"\nPaired devices({lock.get_id()},{thermostat.get_id()}) to hub:{hub2.get_id()}"
    )

    print(f"\nGetting device states from hub: {hub2.get_id()}")
    lock_info = hub_service.device_info(lock.get_id())
    print(f"Lock info: {lock_info}")
    thermostat_info = hub_service.device_info(thermostat.get_id())
    print(f"Thermostat_info info: {thermostat_info}")

    print("\nRemoving device from hub...")
    hub_service.remove_device_from_hub(switch.get_id())
    print(f"Removed switch: {switch.get_id()} from hub: {hub1.get_id()}")

    print("\nTrying to delete paired device (should fail)...")
    success = device_service.delete(dimmer.get_id())
    print(
        f"Delete paired dimmer: {'Success' if success else 'Failed (device is paired)'}"
    )

    print("\nTrying to delete unpaired device (should succeed)...")
    success = device_service.delete(switch.get_id())
    print(f"Delete unpaired switch: {'Success' if success else 'Failed'}")

    print("\nFinal device list...")

    for device in device_service.list_devices():
        print(f"Device:{device.get_info()}")

    print("\n=== Demo Complete ===")
