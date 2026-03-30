import pytest
from src.manager import Manager
from src.models import Parameters, Apartment, Bill, TenantSettlement, Tenant
def test_get_apartment_costs():
    Manager.load_data = lambda self: None
    manager = Manager(Parameters())
    manager.apartments = {'A1': Apartment(key='A1', name='', location='', area_m2=0, rooms={})}
    manager.bills = [
        Bill(amount_pln=200.0, date_due='', apartment='A1', settlement_year=2024, settlement_month=3, type=''),
        Bill(amount_pln=250.0, date_due='', apartment='A1', settlement_year=2024, settlement_month=3, type=''),
        Bill(amount_pln=100.0, date_due='', apartment='A1', settlement_year=2024, settlement_month=4, type='')
    ]
    assert manager.get_apartment_costs('A1', 2024, 3) == 450.0
    assert manager.get_apartment_costs('A1', 2024, 5) == 0.0
    assert manager.get_apartment_costs('A2', 2024, 3) is None
    assert manager.get_apartment_costs('A1', 2024) == 550.0
    assert manager.get_apartment_costs('A1') == 550.0
    with pytest.raises(ValueError):
        manager.get_apartment_costs('A1', 2024, 13)
    with pytest.raises(ValueError):
        manager.get_apartment_costs('A1', 2024, 0)
  from src.models import Tenant, ApartmentSettlement

def test_generate_apartment_settlement():
    Manager.load_data = lambda self: None
    manager = Manager(Parameters())
    manager.apartments = {
        'A1': Apartment(key='A1', name='', location='', area_m2=0, rooms={}),
        'A2': Apartment(key='A2', name='', location='', area_m2=0, rooms={})
    }
    manager.tenants = {
        'T1': Tenant(name='', apartment='A1', room='', rent_pln=1000.0, deposit_pln=0.0, date_agreement_from='', date_agreement_to=''),
        'T2': Tenant(name='', apartment='A1', room='', rent_pln=1200.0, deposit_pln=0.0, date_agreement_from='', date_agreement_to='')
    }
    manager.bills = [
        Bill(amount_pln=300.0, date_due='', apartment='A1', settlement_year=2024, settlement_month=3, type=''),
        Bill(amount_pln=200.0, date_due='', apartment='A1', settlement_year=2024, settlement_month=3, type='')
    ]
    settlement_a1 = manager.generate_apartment_settlement('A1', 2024, 3)
    assert isinstance(settlement_a1, ApartmentSettlement)
    assert settlement_a1.apartment == 'A1'
    assert settlement_a1.month == 3
    assert settlement_a1.year == 2024
    assert settlement_a1.total_bills_pln == 500.0
    assert settlement_a1.total_rent_pln == 2200.0
    assert settlement_a1.total_due_pln == 2700.0
    settlement_a2 = manager.generate_apartment_settlement('A2', 2024, 3)
    assert settlement_a2.apartment == 'A2'
    assert settlement_a2.month == 3
    assert settlement_a2.year == 2024
    assert settlement_a2.total_bills_pln == 0.0
    assert settlement_a2.total_rent_pln == 0.0
    assert settlement_a2.total_due_pln == 0.0