#------------------------------------------------------------------------
#create material classes, and add properties. INCLUDE UNIT!!!!!!!!!
#MUST BE DUCTILE
#MUST HAVE (QUASI) ISENTROPIC PROPERTIES
#------------------------------------------------------------------------

class Material:
    def __init__(self, E, G, Density, Yield_Shear, Yield_Stress):
        self.E = E                  # Young's Modulus (Pa)
        self.G = G                  # Shear Modulus (Pa)
        self.Density = Density      # Density (kg/m³)
        self.Yield_Shear = Yield_Shear  # Shear yield strength (Pa)
        self.Yield_Stress = Yield_Stress # Tensile yield strength (Pa)

    def __repr__(self):
        return (f"{self.__class__.__name__}(E={self.E}, G={self.G}, Density={self.Density}, "
                f"Yield_Shear={self.Yield_Shear}, Yield_Stress={self.Yield_Stress})")



class AL(Material):
    def __init__(self):
        super().__init__(
            E=70e9,              # Young's modulus for aluminum in Pascals
            G=26e9,              # Shear modulus
            Density=2700,        # kg/m³
            Yield_Shear=250e6,   # Pa
            Yield_Stress=300e6   # Pa
        )



class Steel(Material):
    def __init__(self):
        super().__init__(
            E=200e9,             # Young's modulus for steel in Pascals
            G=79.3e9,            # Shear modulus for steel in Pascals
            Density=7850,        # Density of steel in kg/m³
            Yield_Shear=250e6,   # Shear yield strength (typical value) in Pascals
            Yield_Stress=250e6   # Tensile yield strength (e.g., mild steel) in Pascals
        )



class DogshitTestMaterial(Material):
    def __init__(self):
        super().__init__(
            E=200e6,             # Young's modulus for steel in Pascals
            G=79.3e6,            # Shear modulus for steel in Pascals
            Density=1000,        # Density of steel in kg/m³
            Yield_Shear=250e2,   # Shear yield strength (typical value) in Pascals
            Yield_Stress=300e2   # Tensile yield strength (e.g., mild steel) in Pascals
        )


class PLA3DPrintMaterial(Material):
    def __init__(self):
        super().__init__(
            E=3.5e9,     # Young's modulus for PLA in Pascals (approx. 3.5 GPa)
            G=1.3e9,     # Shear modulus for PLA in Pascals (approx. 1.3 GPa, often E / (2*(1+nu)) with nu ~ 0.35)
            Density=1240, # Density of PLA in kg/m³ (approx. 1240 kg/m³)
            Yield_Shear=40e6, # Shear yield strength for PLA in Pascals (approx. 40 MPa, often estimated as 0.6 * Yield_Stress)
            Yield_Stress=60e6 # Tensile yield strength for PLA in Pascals (approx. 60 MPa)
        )

class NaturalFibre(Material):
    def __init__(self):
        super().__init__(
            E=3.5e9,     # Young's modulus for PLA in Pascals (approx. 3.5 GPa)
            G=1.3e9,     # Shear modulus for PLA in Pascals (approx. 1.3 GPa, often E / (2*(1+nu)) with nu ~ 0.35)
            Density=1324, # Density of PLA in kg/m³ (approx. 1240 kg/m³)
            Yield_Shear=70e6, # Shear yield strength for PLA in Pascals (approx. 40 MPa, often estimated as 0.6 * Yield_Stress)
            Yield_Stress=150e6 # Tensile yield strength for PLA in Pascals (approx. 60 MPa)
        )

class Aluminum2024T4(Material):
    def __init__(self):
        super().__init__(
            E=7.31e10,           # Young's modulus in Pascals
            G=2.80e10,           # Shear modulus in Pascals
            Density=2780,        # Density in kg/m³
            Yield_Shear=2.83e8,  # Shear yield strength in Pascals
            Yield_Stress=3.24e8  # Tensile yield strength in Pascals
        )


class Aluminum7075T6(Material):
    def __init__(self):
        super().__init__(
            E=7.00e10,           # Young's modulus in Pascals
            G=2.60e10,           # Shear modulus in Pascals
            Density=3000,        # Density in kg/m³
            Yield_Shear=3.30e8,  # Shear yield strength in Pascals
            Yield_Stress=4.80e8  # Tensile yield strength in Pascals
        )


class Steel300M(Material):
    def __init__(self):
        super().__init__(
            E=2.05e11,           # Young's modulus in Pascals
            G=8.00e10,           # Shear modulus in Pascals
            Density=7890,        # Density in kg/m³
            Yield_Shear=1.36e9,  # Shear yield strength in Pascals
            Yield_Stress=1.59e9  # Tensile yield strength in Pascals
        )


class TitaniumTi6Al4V(Material):
    def __init__(self):
        super().__init__(
            E=1.14e11,           # Young's modulus in Pascals
            G=4.40e10,           # Shear modulus in Pascals
            Density=4430,        # Density in kg/m³
            Yield_Shear=5.50e8,  # Shear yield strength in Pascals
            Yield_Stress=8.80e8  # Tensile yield strength in Pascals
        )

