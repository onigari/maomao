
public class AbsFac2 {

    public static void main(String[] args) {
        Company nvidia = new NVIDIA();
        Company amd = new AMD();
        Company msi = new MSI();

        GPU rtx = nvidia.createGPU();
        rtx.assemble();
        Monitor m1 = amd.createMonitor();
        m1.assemble();

        msi.createGPU().assemble();
        msi.createMonitor().assemble();
    }
}

interface GPU {

    void assemble();
}

class RTX_GPU implements GPU {

    @Override
    public void assemble() {
        System.out.println("Assembling RTX GPU");
    }

}

class AMD_GPU implements GPU {

    @Override
    public void assemble() {
        System.out.println("Assembling AMD GPU");
    }

}

class MSI_GPU implements GPU {

    @Override
    public void assemble() {
        System.out.println("Assembling MSI GPU");
    }

}


interface Monitor {

    void assemble();
}

class RTX_Monitor implements Monitor {

    @Override
    public void assemble() {
        System.out.println("Assembling RTX Monitor");
    }

}

class AMD_Monitor implements Monitor {

    @Override
    public void assemble() {
        System.out.println("Assembling AMD Monitor");
    }

}

class MSI_Monitor implements Monitor {

    @Override
    public void assemble() {
        System.out.println("Assembling MSI Monitor");
    }

}


abstract class Company {

    public GPU assembleGPU() {
        GPU gpu = createGPU();
        gpu.assemble();
        return gpu;
    }

    public abstract GPU createGPU();
    public abstract Monitor createMonitor();
}

class NVIDIA extends Company {

    @Override
    public GPU createGPU() {
        return new RTX_GPU();
    }

    @Override
    public Monitor createMonitor() {
        return new RTX_Monitor();
    }
}

class AMD extends Company {

    @Override
    public GPU createGPU() {
        return new AMD_GPU();
    }

    @Override
    public Monitor createMonitor() {
        return new AMD_Monitor();
    }
}

class MSI extends Company {

    @Override
    public GPU createGPU() {
        return new MSI_GPU();
    }
    
    @Override
    public Monitor createMonitor() {
        return new MSI_Monitor();
    }

}
