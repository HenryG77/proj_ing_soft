import unittest
from datetime import date
from decimal import Decimal

from models import Prestamo


class AmortizacionTests(unittest.TestCase):
    def test_generar_tabla_amortizacion_cierra_saldo(self):
        filas = Prestamo.generar_tabla_amortizacion(
            monto=Decimal("1000.00"),
            tasa_interes=Decimal("12.00"),
            cantidad_cuotas=3,
            fecha_desembolso=date(2026, 1, 1),
        )

        self.assertEqual(len(filas), 3)
        self.assertEqual(sum(fila["capital"] for fila in filas), Decimal("1000.00"))
        self.assertEqual(filas[-1]["saldo_restante"], Decimal("0.00"))

    def test_fecha_vencimiento_pasa_a_lunes_si_es_domingo(self):
        fecha = Prestamo._calcular_fecha_vencimiento(date(2026, 1, 4))
        self.assertEqual(fecha.weekday(), 0)


if __name__ == "__main__":
    unittest.main()
