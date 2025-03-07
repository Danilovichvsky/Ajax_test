import pytest
from scanner_handler import CheckQr


class Check_qr(CheckQr):
    def __init__(self):
        super().__init__()

    def check_in_db(self, qr):
        db_device = {"d1": "123", "d2": "12345", "d3": "1234567"}
        try:
            if qr in db_device.values():
                return True

        except ConnectionError("error with connection to DB"):
            raise ConnectionError

    def check_scanned_device(self, qr: str):
        for func in self.scan_check_out_list(qr):
            result = func()
            if result:  # If an error occurs, return the result immediately
                return result
        message = f"hallelujah {qr}"  # If no errors, pass to can_add_device
        return self.can_add_device(message)  # Return the result of can_add_device


class TestQr:

    @pytest.mark.parametrize('qr,res',
                             [
                                 ('123', 'Red'),
                                 ('12345', 'Green'),
                                 ('1234567', 'Fuzzy Wuzzy'),
                                 ('1234', None)
                             ])
    def test_check_len_color(self, qr, res):
        obj_qr = Check_qr()
        assert obj_qr.check_len_color(qr) == res

    @pytest.mark.parametrize('qr,message',
                             [
                                 ('123', 'hallelujah 123'),
                                 ('12345', 'hallelujah 12345'),
                                 ('1234544', ['Not in DB']),
                                 ('12345444', ['Error: Wrong qr length 8']),
                             ])
    def test_success_scanned_device(self, qr, message):
        check_qr = Check_qr()
        result = check_qr.check_scanned_device(qr)
        assert result == message
