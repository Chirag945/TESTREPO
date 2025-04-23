
        
        @Override
        public void stop() {
            running = false;
            System.out.println("Vehicle stopping");
        }
        
        public static List<String> getValidTypes() {
            return VALID_TYPES;
        }
    }

    @Component
    public class ElectricCar extends AbstractVehicle {
        private transient int batteryLevel;
        @Deprecated
        private String oldField;
        
        public static class Battery {
            private final int capacity;
            
            public Battery(int capacity) {
                this.capacity = capacity;
            }
            
            public int getCapacity() {
                return capacity;
            }
        }
        
        private final Battery battery;
        
        public ElectricCar(String manufacturer, int batteryCapacity) {
            super(manufacturer);
            this.battery = new Battery(batteryCapacity);
            this.batteryLevel = 100;
        }
        
        @Override
        public String getType() {
 
        
        @Deprecated
        public void oldMethod() throws IllegalStateException {
            throw new IllegalStateException("This method is deprecated");
        }
    }"""
