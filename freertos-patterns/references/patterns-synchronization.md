# Synchronization Patterns

## Mutex (Mutual Exclusion)

```cpp
SemaphoreHandle_t i2cMutex;

void taskSensorA(void* parameter) {
  while(true) {
    // Acquire mutex before I2C access
    if (xSemaphoreTake(i2cMutex, pdMS_TO_TICKS(1000)) == pdPASS) {
      // Protected I2C transaction
      Wire.beginTransmission(0x76);
      Wire.write(0xF7);
      Wire.endTransmission();
      
      Serial.println("Sensor A read complete");
      
      // Release mutex
      xSemaphoreGive(i2cMutex);
    } else {
      Serial.println("Sensor A: Mutex timeout!");
    }
    
    vTaskDelay(pdMS_TO_TICKS(500));
  }
}

void taskSensorB(void* parameter) {
  while(true) {
    if (xSemaphoreTake(i2cMutex, pdMS_TO_TICKS(1000)) == pdPASS) {
      Wire.beginTransmission(0x77);
      Wire.write(0x00);
      Wire.endTransmission();
      
      Serial.println("Sensor B read complete");
      
      xSemaphoreGive(i2cMutex);
    } else {
      Serial.println("Sensor B: Mutex timeout!");
    }
    
    vTaskDelay(pdMS_TO_TICKS(700));
  }
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  
  // Create mutex with priority inheritance
  i2cMutex = xSemaphoreCreateMutex();
  
  if (i2cMutex == NULL) {
    Serial.println("Mutex creation failed!");
    while(1);
  }
  
  xTaskCreate(taskSensorA, "SensorA", 4096, NULL, 2, NULL);
  xTaskCreate(taskSensorB, "SensorB", 4096, NULL, 2, NULL);
}
```

## Binary Semaphore (Event Signaling)

```cpp
SemaphoreHandle_t dataReadySemaphore;
float sensorData = 0.0;

void taskProducer(void* parameter) {
  while(true) {
    // Read sensor
    sensorData = analogRead(A0) * (3.3 / 4095.0);
    
    // Signal data ready
    xSemaphoreGive(dataReadySemaphore);
    
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void taskConsumer(void* parameter) {
  while(true) {
    // Wait for data ready signal
    if (xSemaphoreTake(dataReadySemaphore, portMAX_DELAY) == pdPASS) {
      Serial.print("New data: ");
      Serial.println(sensorData, 2);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(A0, INPUT);
  
  // Create binary semaphore (initially empty)
  dataReadySemaphore = xSemaphoreCreateBinary();
  
  xTaskCreate(taskProducer, "Producer", 2048, NULL, 2, NULL);
  xTaskCreate(taskConsumer, "Consumer", 2048, NULL, 1, NULL);
}
```

## Counting Semaphore (Resource Pool)

```cpp
#define NUM_BUFFERS 5

SemaphoreHandle_t bufferSemaphore;
char buffers[NUM_BUFFERS][128];

void taskWriter(void* parameter) {
  int taskID = (int)parameter;
  
  while(true) {
    // Wait for available buffer
    if (xSemaphoreTake(bufferSemaphore, pdMS_TO_TICKS(5000)) == pdPASS) {
      // Find free buffer (simplified - should track properly)
      Serial.printf("Task %d: Got buffer\n", taskID);
      
      // Use buffer
      vTaskDelay(pdMS_TO_TICKS(random(500, 2000)));
      
      // Release buffer
      xSemaphoreGive(bufferSemaphore);
      Serial.printf("Task %d: Released buffer\n", taskID);
    } else {
      Serial.printf("Task %d: No buffers available!\n", taskID);
    }
    
    vTaskDelay(pdMS_TO_TICKS(100));
  }
}

void setup() {
  Serial.begin(115200);
  
  // Create counting semaphore (5 resources)
  bufferSemaphore = xSemaphoreCreateCounting(NUM_BUFFERS, NUM_BUFFERS);
  
  // Create 10 tasks competing for 5 buffers
  for (int i = 0; i < 10; i++) {
    xTaskCreate(taskWriter, "Writer", 2048, (void*)i, 1, NULL);
  }
}
```

## Critical Sections (Short Protection)

```cpp
volatile uint32_t sharedCounter = 0;

void taskIncrement(void* parameter) {
  while(true) {
    // Enter critical section (disables interrupts)
    taskENTER_CRITICAL();
    sharedCounter++;
    uint32_t local = sharedCounter;
    taskEXIT_CRITICAL();
    
    if (local % 1000 == 0) {
      Serial.println(local);
    }
    
    vTaskDelay(pdMS_TO_TICKS(1));
  }
}

void setup() {
  Serial.begin(115200);
  
  xTaskCreate(taskIncrement, "Inc1", 2048, NULL, 1, NULL);
  xTaskCreate(taskIncrement, "Inc2", 2048, NULL, 1, NULL);
}
```

**⚠️ Warning:** Critical sections disable interrupts! Keep duration <10 microseconds.

## Recursive Mutex (Nested Locking)

```cpp
SemaphoreHandle_t recursiveMutex;

void functionNested() {
  // Can be called while mutex already held
  if (xSemaphoreTakeRecursive(recursiveMutex, pdMS_TO_TICKS(1000)) == pdPASS) {
    Serial.println("Nested function executing");
    xSemaphoreGiveRecursive(recursiveMutex);
  }
}

void functionOuter() {
  if (xSemaphoreTakeRecursive(recursiveMutex, pdMS_TO_TICKS(1000)) == pdPASS) {
    Serial.println("Outer function executing");
    
    // Call nested function (reentrant lock)
    functionNested();
    
    xSemaphoreGiveRecursive(recursiveMutex);
  }
}

void taskExample(void* parameter) {
  while(true) {
    functionOuter();
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void setup() {
  Serial.begin(115200);
  
  // Create recursive mutex
  recursiveMutex = xSemaphoreCreateRecursiveMutex();
  
  xTaskCreate(taskExample, "Example", 2048, NULL, 1, NULL);
}
```

## Priority Inheritance (Prevent Inversion)

```cpp
SemaphoreHandle_t resourceMutex;

void taskLowPriority(void* parameter) {
  while(true) {
    Serial.println("LOW: Requesting resource");
    
    if (xSemaphoreTake(resourceMutex, pdMS_TO_TICKS(1000)) == pdPASS) {
      Serial.println("LOW: Got resource, holding 500ms");
      vTaskDelay(pdMS_TO_TICKS(500));  // Long operation
      xSemaphoreGive(resourceMutex);
    }
    
    vTaskDelay(pdMS_TO_TICKS(2000));
  }
}

void taskMediumPriority(void* parameter) {
  while(true) {
    Serial.println("MED: Busy work (no mutex)");
    vTaskDelay(pdMS_TO_TICKS(10));  // CPU-intensive
  }
}

void taskHighPriority(void* parameter) {
  vTaskDelay(pdMS_TO_TICKS(100));  // Let low priority get mutex first
  
  while(true) {
    Serial.println("HIGH: Requesting resource");
    
    // High priority will boost low priority task
    if (xSemaphoreTake(resourceMutex, pdMS_TO_TICKS(1000)) == pdPASS) {
      Serial.println("HIGH: Got resource");
      xSemaphoreGive(resourceMutex);
    }
    
    vTaskDelay(pdMS_TO_TICKS(1500));
  }
}

void setup() {
  Serial.begin(115200);
  
  // Mutex has priority inheritance by default
  resourceMutex = xSemaphoreCreateMutex();
  
  xTaskCreate(taskLowPriority, "Low", 2048, NULL, 1, NULL);
  xTaskCreate(taskMediumPriority, "Med", 2048, NULL, 2, NULL);
  xTaskCreate(taskHighPriority, "High", 2048, NULL, 3, NULL);
}
```

## Semaphore from ISR

```cpp
#define BUTTON_PIN 0

SemaphoreHandle_t buttonSemaphore;

void IRAM_ATTR buttonISR() {
  BaseType_t xHigherPriorityTaskWoken = pdFALSE;
  
  xSemaphoreGiveFromISR(buttonSemaphore, &xHigherPriorityTaskWoken);
  
  if (xHigherPriorityTaskWoken) {
    portYIELD_FROM_ISR();
  }
}

void taskButtonHandler(void* parameter) {
  while(true) {
    if (xSemaphoreTake(buttonSemaphore, portMAX_DELAY) == pdPASS) {
      Serial.println("Button pressed!");
      vTaskDelay(pdMS_TO_TICKS(200));  // Debounce
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  buttonSemaphore = xSemaphoreCreateBinary();
  
  xTaskCreate(taskButtonHandler, "Button", 2048, NULL, 3, NULL);
  
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonISR, FALLING);
}
```

## Deadlock Prevention

### ❌ Deadlock Example (Wrong)
```cpp
// Task A: Lock mutex1 → Lock mutex2
// Task B: Lock mutex2 → Lock mutex1
// = DEADLOCK!
```

### ✅ Correct Pattern (Always Same Order)
```cpp
SemaphoreHandle_t mutex1, mutex2;

void taskA(void* parameter) {
  while(true) {
    xSemaphoreTake(mutex1, portMAX_DELAY);  // Order: 1 then 2
    xSemaphoreTake(mutex2, portMAX_DELAY);
    
    // Critical section
    
    xSemaphoreGive(mutex2);
    xSemaphoreGive(mutex1);
    
    vTaskDelay(pdMS_TO_TICKS(100));
  }
}

void taskB(void* parameter) {
  while(true) {
    xSemaphoreTake(mutex1, portMAX_DELAY);  // Same order: 1 then 2
    xSemaphoreTake(mutex2, portMAX_DELAY);
    
    // Critical section
    
    xSemaphoreGive(mutex2);
    xSemaphoreGive(mutex1);
    
    vTaskDelay(pdMS_TO_TICKS(100));
  }
}
```

## Synchronization Primitive Comparison

| Primitive | Max Count | Priority Inheritance | Use Case |
|-----------|-----------|---------------------|----------|
| **Mutex** | 1 | ✅ Yes | Exclusive resource access |
| **Binary Semaphore** | 1 | ❌ No | Event signaling |
| **Counting Semaphore** | N | ❌ No | Resource pool (N items) |
| **Recursive Mutex** | Unlimited | ✅ Yes | Nested function calls |
| **Critical Section** | N/A | N/A | Very short (<10µs) |

## Best Practices

1. **Always use timeout** - Don't block forever (except proven safe)
2. **Check return values** - pdPASS = success
3. **Minimize lock duration** - <10ms typical, <1ms ideal
4. **Lock ordering** - Always acquire in same order to prevent deadlock
5. **Use mutex for shared data** - Not binary semaphore
6. **Critical sections: <10µs only** - They disable interrupts!
7. **FromISR variants in ISR** - Never use regular take/give in ISR

## Verification Checklist

- [ ] Mutex/semaphore created before use
- [ ] Handle checked for NULL
- [ ] Take/give always paired (no orphaned locks)
- [ ] Timeout appropriate (not portMAX_DELAY unless proven safe)
- [ ] Priority inheritance enabled for shared resources
- [ ] Lock duration minimized (<10ms)
- [ ] FromISR variants used in interrupts
- [ ] No nested locks (or consistent order)
