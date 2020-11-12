class Expr : # abstract class
    def __eq__(a, b):
        a_poly = a.getPolynomial()
        b_poly = b.getPolynomial()
        if a_poly == b_poly:
            return True
        else:
            return False

class Var (Expr) :
    def __init__(self,name) :
        self.name = name
    
    def eval(self,env) :
        return env[self.name]
    
    def __str__(self) :
        return self.name

    def getPolynomial(self):
        var_monomial = Monomial([self.name], 1)
        return Polynomial(var_monomial)


class Const (Expr) :
    def __init__(self,value) :
        self.value = value

    def eval(self,env) :
        return self.value
    def __str__(self) :
        return str(self.value)

    def getPolynomial(self):
        const_monomial = Monomial([], self.value)
        return Polynomial(const_monomial)


class BinOp(Expr) : # abstract class
    def __init__(self,left,right) :
        self.left = left
        self.right = right        
    
    # op(int,int) : int
    
    def eval(self,env) :
        return self.op(self.left.eval(env),self.right.eval(env))

    def __str__(self):
        left_var = self.left
        right_var = self.right
        op_sign = self.op_sign
        return f"{left_var}{op_sign}{right_var}"


class Plus(BinOp) :
    op_sign = '+'

    def op(self,x,y) :
        return x+y

    def __str__(self) :
        return f"({BinOp.__str__(self)})"

    def getPolynomial(self):
        left_poly = self.left.getPolynomial()
        right_poly = self.right.getPolynomial()
        return left_poly + right_poly


class Times(BinOp) :
    op_sign = '*'

    def op(self,x,y) :
        return x*y

    def getPolynomial(self):
        left_poly = self.left.getPolynomial()
        right_poly = self.right.getPolynomial()
        return left_poly * right_poly
    

class Monomial:
    ''' Monomial data structure
    Used to store monomials
    '''
    def __init__(self, power_product, coefficient):
        ''' __init__ intiiates the monomial
        takes input:
        power_product (list)
        coefficient (int (or float))
        '''
        self.pprod = {}
        self.coefficient = coefficient

        for variable in power_product:
            if variable in self.pprod.keys():
                self.pprod[variable] += 1
            else:
                self.pprod[variable] = 1
    
    def __str__(self):
        output_string = str(self.coefficient)
        for key in self.pprod.keys():
            output_string += key
            output_string += '^'
            output_string += str(self.pprod[key])
        return output_string

    def __eq__(a, b):
        if (a.pprod == b.pprod) and (a.coefficient == b.coefficient):
            return True
        else:
            return False


class Polynomial:
    '''
    Polynomial - a list of monomials
    '''
    
    def __init__(self, initial_monomial):
        self.val = [initial_monomial]

    def __str__(self):
        output_string = ''
        for monomial in self.val:
            output_string += monomial.__str__()
            output_string += ' + '
        return output_string[:-3]

    def __add__(a, b):
        ''' Addition of polynomials
        '''
        output_poly = a.makeZeroPolynomial()
        for mono_a in a.val:
            output_poly.addMonomial(mono_a)
        for mono_b in b.val:
            output_poly.addMonomial(mono_b)
        return output_poly

    def __mul__(a, b):
        ''' Cross multiplication of polynomials
        '''
        output_poly = a.makeZeroPolynomial()
        for mono_a in a.val:
            for mono_b in b.val:
                c = output_poly.multiply(mono_a, mono_b)
                output_poly.addMonomial(c)
        return output_poly

    def __eq__(a, b):
        for a_monomial in a.val:
            if a_monomial not in b.val:
                return False
        for b_monomial in b.val:
            if b_monomial not in a.val:
                return False
        return True

    def makeZeroPolynomial(self):
        return Polynomial(Monomial([], 0))

    def addMonomial(self, addition_monomial):
        '''
        addMonomial - takes a monomial, and adds to this polynomial
        '''
        for monomial in self.val:
            if addition_monomial.pprod == monomial.pprod:
                monomial.coefficient += addition_monomial.coefficient
                return
        self.val.append(addition_monomial)

    def multiply(self, a, b):
        c_pprod = {}
        c_coeffficient = a.coefficient * b.coefficient
        pprod_a, pprod_b = a.pprod, b.pprod
        a_keys, b_keys = pprod_a.keys(), pprod_b.keys()
        for key in a_keys:
            if key in b_keys:
                c_pprod[key] = pprod_a[key] + pprod_b[key]
            else:
                c_pprod[key] = pprod_a[key]
        for key in b_keys:
            if key not in a_keys:
                c_pprod[key] = pprod_b[key]
        c = Monomial([],0)
        c.pprod = c_pprod
        c.coefficient = c_coeffficient
        return c

e1 = Times(
    Plus(
        Var("x"),
        Const(2)
        ),
    Var("y")
    )

e2 = Plus(
    Var("x"),
    Times(
        Const(2),
        Var("y")
        )
    )

e3 = Plus(
    Times(
        Var("x"),
        Var("x")
        ),
    Plus(
        Times(Var("x"),Var("y")),
        Times(
            Var("y"),
            Times(
                Var("y"),
                Var("y")
                )
            )
        )
    )

e4 = Plus(
    Times(
        Var("x"),
        Var("x")
        ),
    Plus(
        Times(Var("x"),Var("y")),
        Times(
            Var("y"),
            Plus(
                Var("y"),
                Var("y")
                )
            )
        )
    )

e5 = Plus(
    Times(
        Var("x"),
        Var("x")
    ),
    Plus(
        Times(
            Const(3),
            Var("x")
        ),
        Const(2)
    )
)

e6 = Times(
    Plus(
        Var("x"),
        Const(2)
    ),
    Plus(
        Var("x"),
        Const(1)
    )
)

env_data = {
    'x': 2,
    'y': 3
}

e7 = Times(
    Var("x"),
    Var("y")
    )

e8 = Times(
    Var("y"),
    Var("x")
)


print(f"e1 - {str(e1)} -> {e1.getPolynomial()}")
print(f"e2 - {str(e2)} -> {e2.getPolynomial()}")
print(f"e3 - {str(e3)} -> {e3.getPolynomial()}")
print(f"e4 - {str(e4)} -> {e4.getPolynomial()}")
print(f"e5 - {str(e5)} -> {e5.getPolynomial()}")
print(f"e6 - {str(e6)} -> {e6.getPolynomial()}")
print(f"e7 - {str(e7)} -> {e7.getPolynomial()}")
print(f"e8 - {str(e8)} -> {e8.getPolynomial()}")