#create material classes, and add properties. INCLUDE UNIT!!!!!!!!!

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
            Density=7850,        # Density of steel in kg/m³
            Yield_Shear=250e2,   # Shear yield strength (typical value) in Pascals
            Yield_Stress=250e2   # Tensile yield strength (e.g., mild steel) in Pascals
        )
