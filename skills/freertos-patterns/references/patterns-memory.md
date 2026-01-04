# Memory Management Patterns

## Heap Monitoring

```cpp
void printHeapStats() {
  uint32_t freeHeap = ESP.getFreeHeap();
  uint32_t minFreeHeap = ESP.getMinFreeHeap();
  uint32_t heapSize = ESP.getHeapSize();
  
  Serial.println("=== Heap Statistics ===");
  Serial.printf("Free: %d bytes (%.1f%%)\n", freeHeap, (freeHeap * 100.0) / heapSize);
  Serial.printf("Min Free: %d bytes\n", minFreeHeap);
  Serial.printf("Total Size: %d bytes\n", heapSize);
  
  if (freeHeap < 10000) {
    Serial.println("WARNING: Low heap!");
  }
}

void loop() {
  printHeapStats();
  vTaskDelay(pdMS_TO_TICKS(5000));
}
```

## Stack High Water Mark

```cpp
TaskHandle_t task1Handle, task2Handle;

void printStackStats() {
  UBaseType_t freeStack1 = uxTaskGetStackHighWaterMark(task1Handle);
  UBaseType_t freeStack2 = uxTaskGetStackHighWaterMark(task2Handle);
  
  Serial.println("=== Stack Statistics ===");
  Serial.printf("Task1 free: %d bytes\n", freeStack1 * sizeof(StackType_t));
  Serial.printf("Task2 free: %d bytes\n", freeStack2 * sizeof(StackType_t));
  
  if (freeStack1 < 512 / sizeof(StackType_t)) {
    Serial.println("WARNING: Task1 stack low!");
  }
  if (freeStack2 < 512 / sizeof(StackType_t)) {
    Serial.println("WARNING: Task2 stack low!");
  }
}

void loop() {
  printStackStats();
  vTaskDelay(pdMS_TO_TICKS(5000));
}
```

## Dynamic Memory Allocation

```cpp
void taskWithDynamicMemory(void* parameter) {
  while(true) {
    // Allocate memory
    uint8_t* buffer = (uint8_t*)pvPortMalloc(1024);
    
    if (buffer == NULL) {
      Serial.println("Memory allocation failed!");
      vTaskDelay(pdMS_TO_TICKS(1000));
      continue;
    }
    
    // Use buffer
    memset(buffer, 0xAA, 1024);
    Serial.println("Buffer allocated and used");
    
    // Free memory
    vPortFree(buffer);
    
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void setup() {
  Serial.begin(115200);
  xTaskCreate(taskWithDynamicMemory, "Dynamic", 4096, NULL, 1, NULL);
}
```

**⚠️ Prefer static allocation when possible** - Less fragmentation, predictable behavior.

## Static Allocation (No Heap)

```cpp
#define TASK_STACK_SIZE 2048

StaticTask_t taskBuffer;
StackType_t taskStack[TASK_STACK_SIZE];

void taskStatic(void* parameter) {
  while(true) {
    Serial.println("Static task running");
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void setup() {
  Serial.begin(115200);
  
  // Create task with static buffers (no heap allocation)
  TaskHandle_t handle = xTaskCreateStatic(
    taskStatic,
    "Static",
    TASK_STACK_SIZE,
    NULL,
    1,
    taskStack,
    &taskBuffer
  );
  
  if (handle == NULL) {
    Serial.println("Static task creation failed!");
  }
}
```

## Memory Pool Pattern

```cpp
#define POOL_SIZE 10
#define BUFFER_SIZE 128

struct Buffer {
  uint8_t data[BUFFER_SIZE];
  bool inUse;
};

Buffer memoryPool[POOL_SIZE];
SemaphoreHandle_t poolMutex;

Buffer* allocateBuffer() {
  Buffer* result = NULL;
  
  if (xSemaphoreTake(poolMutex, pdMS_TO_TICKS(1000)) == pdPASS) {
    for (int i = 0; i < POOL_SIZE; i++) {
      if (!memoryPool[i].inUse) {
        memoryPool[i].inUse = true;
        result = &memoryPool[i];
        break;
      }
    }
    xSemaphoreGive(poolMutex);
  }
  
  return result;
}

void freeBuffer(Buffer* buffer) {
  if (xSemaphoreTake(poolMutex, pdMS_TO_TICKS(1000)) == pdPASS) {
    buffer->inUse = false;
    xSemaphoreGive(poolMutex);
  }
}

void taskUser(void* parameter) {
  while(true) {
    Buffer* buf = allocateBuffer();
    
    if (buf != NULL) {
      // Use buffer
      memset(buf->data, 0, BUFFER_SIZE);
      Serial.println("Buffer allocated");
      
      vTaskDelay(pdMS_TO_TICKS(500));
      
      // Free buffer
      freeBuffer(buf);
      Serial.println("Buffer freed");
    } else {
      Serial.println("No buffers available!");
    }
    
    vTaskDelay(pdMS_TO_TICKS(200));
  }
}

void setup() {
  Serial.begin(115200);
  
  // Initialize pool
  for (int i = 0; i < POOL_SIZE; i++) {
    memoryPool[i].inUse = false;
  }
  
  poolMutex = xSemaphoreCreateMutex();
  
  // Create multiple tasks using pool
  xTaskCreate(taskUser, "User1", 2048, NULL, 1, NULL);
  xTaskCreate(taskUser, "User2", 2048, NULL, 1, NULL);
  xTaskCreate(taskUser, "User3", 2048, NULL, 1, NULL);
}
```

## Stack Overflow Detection

Enable in Arduino IDE → Tools → Core Debug Level → Verbose

```cpp
// Hook called when stack overflow detected
extern "C" void vApplicationStackOverflowHook(TaskHandle_t xTask, char* pcTaskName) {
  Serial.print("STACK OVERFLOW in task: ");
  Serial.println(pcTaskName);
  
  // Print task info
  UBaseType_t freeStack = uxTaskGetStackHighWaterMark(xTask);
  Serial.printf("Free stack: %d bytes\n", freeStack * sizeof(StackType_t));
  
  // Halt system
  while(1) {
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    delay(100);
  }
}
```

## Heap Usage Analysis

```cpp
void analyzeHeapUsage() {
  uint32_t heapBefore = ESP.getFreeHeap();
  
  // Allocate test buffer
  uint8_t* testBuffer = (uint8_t*)malloc(1024);
  
  uint32_t heapAfter = ESP.getFreeHeap();
  uint32_t overhead = (heapBefore - heapAfter) - 1024;
  
  Serial.printf("Heap overhead: %d bytes per allocation\n", overhead);
  
  free(testBuffer);
  
  // Check fragmentation
  uint32_t heapRestored = ESP.getFreeHeap();
  if (heapRestored < heapBefore) {
    Serial.printf("Heap fragmentation: %d bytes lost\n", heapBefore - heapRestored);
  }
}
```

## PSRAM Support (ESP32 with External RAM)

```cpp
void taskWithPSRAM(void* parameter) {
  // Allocate from PSRAM (external RAM)
  uint8_t* largeBuf = (uint8_t*)ps_malloc(100 * 1024);  // 100KB
  
  if (largeBuf == NULL) {
    Serial.println("PSRAM allocation failed!");
    vTaskDelete(NULL);
  }
  
  Serial.println("PSRAM buffer allocated");
  
  // Use buffer
  memset(largeBuf, 0, 100 * 1024);
  
  // Free
  free(largeBuf);
  
  vTaskDelete(NULL);
}

void setup() {
  Serial.begin(115200);
  
  // Check if PSRAM available
  if (psramFound()) {
    Serial.printf("PSRAM size: %d bytes\n", ESP.getPsramSize());
    Serial.printf("PSRAM free: %d bytes\n", ESP.getFreePsram());
    
    xTaskCreate(taskWithPSRAM, "PSRAM", 2048, NULL, 1, NULL);
  } else {
    Serial.println("PSRAM not available");
  }
}
```

## Memory Leak Detection

```cpp
uint32_t baselineHeap;

void setup() {
  Serial.begin(115200);
  
  // Wait for tasks to stabilize
  vTaskDelay(pdMS_TO_TICKS(5000));
  
  // Record baseline
  baselineHeap = ESP.getFreeHeap();
  Serial.printf("Baseline heap: %d bytes\n", baselineHeap);
}

void loop() {
  uint32_t currentHeap = ESP.getFreeHeap();
  int32_t delta = currentHeap - baselineHeap;
  
  Serial.printf("Heap delta: %d bytes\n", delta);
  
  if (delta < -10000) {
    Serial.println("WARNING: Possible memory leak!");
  }
  
  vTaskDelay(pdMS_TO_TICKS(10000));
}
```

## Fragmentation Test

```cpp
void testFragmentation() {
  const int numAllocs = 100;
  void* pointers[numAllocs];
  
  uint32_t heapBefore = ESP.getFreeHeap();
  
  // Allocate many small blocks
  for (int i = 0; i < numAllocs; i++) {
    pointers[i] = malloc(64);
  }
  
  // Free every other block
  for (int i = 0; i < numAllocs; i += 2) {
    free(pointers[i]);
  }
  
  // Try to allocate large block
  uint32_t largeSize = 4096;
  void* largeBuf = malloc(largeSize);
  
  if (largeBuf == NULL) {
    Serial.println("Fragmentation detected: Can't allocate large block");
  } else {
    Serial.println("No fragmentation");
    free(largeBuf);
  }
  
  // Cleanup
  for (int i = 1; i < numAllocs; i += 2) {
    free(pointers[i]);
  }
  
  uint32_t heapAfter = ESP.getFreeHeap();
  Serial.printf("Heap recovered: %d / %d bytes\n", heapAfter, heapBefore);
}
```

## Safe Buffer Sizing

```cpp
// Calculate required buffer size with safety margin
#define SENSOR_DATA_SIZE 128
#define SAFETY_MARGIN 1.5  // 50% margin

#define BUFFER_SIZE ((int)(SENSOR_DATA_SIZE * SAFETY_MARGIN))

void taskSafeBuffer(void* parameter) {
  char buffer[BUFFER_SIZE];
  
  while(true) {
    int written = snprintf(buffer, BUFFER_SIZE, "Sensor data: %lu", millis());
    
    if (written >= BUFFER_SIZE) {
      Serial.println("WARNING: Buffer truncation!");
    } else {
      Serial.println(buffer);
    }
    
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}
```

## Heap Integrity Check

```cpp
void checkHeapIntegrity() {
  // ESP32-specific heap check
  if (!heap_caps_check_integrity_all(true)) {
    Serial.println("HEAP CORRUPTION DETECTED!");
    
    // Print heap info
    heap_caps_print_heap_info(MALLOC_CAP_DEFAULT);
    
    // Halt
    while(1);
  } else {
    Serial.println("Heap integrity: OK");
  }
}

void loop() {
  checkHeapIntegrity();
  vTaskDelay(pdMS_TO_TICKS(30000));
}
```

## Memory Guidelines

### Heap Sizing
```
ESP32 Total SRAM: 520KB
- WiFi stack: ~40KB
- System overhead: ~20KB
- FreeRTOS kernel: ~8KB
- Available: ~450KB

Safe allocation: 80% of available = 360KB
```

### Stack Sizing
| Task Type | Recommended Stack |
|-----------|-------------------|
| Simple LED blink | 1024 bytes |
| Serial I/O | 2048 bytes |
| WiFi/Network | 4096 bytes |
| JSON parsing | 8192 bytes |
| Large buffers | 16384 bytes |

### Formula
```
Stack Size = LocalVars + CallChain + Margin

Example:
- char buffer[1024]
- 3 function calls (256 bytes each)
- 50% margin
Total: 1024 + 768 + 896 = 2688 → Round to 3072 (3KB)
```

## Best Practices

1. **Monitor heap continuously** - Check every 5-10 seconds
2. **Prefer static allocation** - Avoid malloc/new in tasks
3. **Use memory pools** - For fixed-size allocations
4. **Check high water mark** - Stack usage monitoring
5. **Enable overflow detection** - Catch stack issues early
6. **Free immediately** - Don't hold memory longer than needed
7. **Use PSRAM for large buffers** - If available (ESP32-WROVER)
8. **Avoid fragmentation** - Allocate/free in patterns, not randomly

## Verification Checklist

- [ ] Heap monitored every 5-10 seconds
- [ ] Stack high water marks checked
- [ ] Stack overflow detection enabled
- [ ] All malloc/new calls checked for NULL
- [ ] All allocated memory freed
- [ ] No memory leaks after 1 hour runtime
- [ ] Heap remains above 20% free
- [ ] Stack remains above 20% free per task
- [ ] Large buffers (>4KB) justified
