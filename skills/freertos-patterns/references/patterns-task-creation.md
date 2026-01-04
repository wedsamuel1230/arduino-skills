# Task Creation & Lifecycle Patterns

## Basic Task Creation

```cpp
TaskHandle_t myTaskHandle;

void myTask(void* parameter) {
  // Task initialization
  pinMode(LED_BUILTIN, OUTPUT);
  
  while(true) {
    // Task main loop
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
  
  // Task cleanup (if exiting)
  vTaskDelete(NULL);
}

void setup() {
  BaseType_t result = xTaskCreate(
    myTask,              // Task function
    "MyTask",            // Name (max 16 chars)
    2048,                // Stack size (bytes)
    NULL,                // Parameters
    1,                   // Priority (0 = lowest, 24 = highest)
    &myTaskHandle        // Task handle (optional)
  );
  
  if (result != pdPASS) {
    Serial.println("Task creation failed!");
  }
}
```

## Task with Parameters

```cpp
struct TaskParams {
  int ledPin;
  unsigned long interval;
};

void taskBlink(void* pvParameters) {
  TaskParams* params = (TaskParams*)pvParameters;
  pinMode(params->ledPin, OUTPUT);
  
  while(true) {
    digitalWrite(params->ledPin, HIGH);
    vTaskDelay(pdMS_TO_TICKS(params->interval));
    digitalWrite(params->ledPin, LOW);
    vTaskDelay(pdMS_TO_TICKS(params->interval));
  }
}

void setup() {
  static TaskParams led1Params = {LED_BUILTIN, 500};
  static TaskParams led2Params = {2, 1000};
  
  xTaskCreate(taskBlink, "LED1", 2048, &led1Params, 1, NULL);
  xTaskCreate(taskBlink, "LED2", 2048, &led2Params, 1, NULL);
}
```

## Core Pinning (ESP32 Dual-Core)

```cpp
void taskCore0(void* parameter) {
  while(true) {
    Serial.print("Running on core: ");
    Serial.println(xPortGetCoreID());
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void taskCore1(void* parameter) {
  while(true) {
    Serial.print("Running on core: ");
    Serial.println(xPortGetCoreID());
    vTaskDelay(pdMS_TO_TICKS(1500));
  }
}

void setup() {
  Serial.begin(115200);
  
  // Pin to Core 0 (protocol/WiFi stack)
  xTaskCreatePinnedToCore(taskCore0, "Core0", 2048, NULL, 1, NULL, 0);
  
  // Pin to Core 1 (application)
  xTaskCreatePinnedToCore(taskCore1, "Core1", 2048, NULL, 1, NULL, 1);
}
```

## Priority Demonstration

```cpp
void taskLowPriority(void* parameter) {
  while(true) {
    Serial.println("LOW priority task");
    vTaskDelay(pdMS_TO_TICKS(100));
  }
}

void taskHighPriority(void* parameter) {
  while(true) {
    Serial.println("HIGH priority task");
    vTaskDelay(pdMS_TO_TICKS(100));
  }
}

void setup() {
  Serial.begin(115200);
  
  // Low priority runs less often
  xTaskCreate(taskLowPriority, "Low", 2048, NULL, 1, NULL);
  
  // High priority preempts low priority
  xTaskCreate(taskHighPriority, "High", 2048, NULL, 5, NULL);
}
```

## Stack Monitoring

```cpp
TaskHandle_t taskHandle;

void taskMonitored(void* parameter) {
  // Local variable (consumes stack)
  char buffer[512];
  
  while(true) {
    snprintf(buffer, sizeof(buffer), "Task running");
    Serial.println(buffer);
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void loop() {
  // Monitor stack usage
  UBaseType_t freeWords = uxTaskGetStackHighWaterMark(taskHandle);
  uint32_t freeBytes = freeWords * sizeof(StackType_t);
  
  Serial.print("Free stack: ");
  Serial.print(freeBytes);
  Serial.println(" bytes");
  
  vTaskDelay(pdMS_TO_TICKS(5000));
}

void setup() {
  Serial.begin(115200);
  xTaskCreate(taskMonitored, "Monitor", 2048, NULL, 1, &taskHandle);
}
```

## Task Suspension & Resumption

```cpp
TaskHandle_t workerTask;

void taskWorker(void* parameter) {
  while(true) {
    Serial.println("Working...");
    vTaskDelay(pdMS_TO_TICKS(500));
  }
}

void taskController(void* parameter) {
  bool suspended = false;
  
  while(true) {
    vTaskDelay(pdMS_TO_TICKS(3000));
    
    if (suspended) {
      Serial.println("Resuming worker");
      vTaskResume(workerTask);
    } else {
      Serial.println("Suspending worker");
      vTaskSuspend(workerTask);
    }
    
    suspended = !suspended;
  }
}

void setup() {
  Serial.begin(115200);
  xTaskCreate(taskWorker, "Worker", 2048, NULL, 1, &workerTask);
  xTaskCreate(taskController, "Control", 2048, NULL, 2, NULL);
}
```

## Graceful Task Deletion

```cpp
TaskHandle_t taskHandle;
volatile bool shouldExit = false;

void taskGraceful(void* parameter) {
  // Allocate resources
  uint8_t* buffer = (uint8_t*)malloc(1024);
  
  while(!shouldExit) {
    // Do work
    Serial.println("Task running");
    vTaskDelay(pdMS_TO_TICKS(500));
  }
  
  // Cleanup before exit
  free(buffer);
  Serial.println("Task exiting gracefully");
  
  vTaskDelete(NULL);
}

void setup() {
  Serial.begin(115200);
  xTaskCreate(taskGraceful, "Graceful", 4096, NULL, 1, &taskHandle);
  
  // Signal task to exit after 5 seconds
  delay(5000);
  shouldExit = true;
}
```

## Task State Monitoring

```cpp
void printTaskState(TaskHandle_t handle, const char* name) {
  eTaskState state = eTaskGetState(handle);
  
  Serial.print(name);
  Serial.print(": ");
  
  switch(state) {
    case eRunning:   Serial.println("Running"); break;
    case eReady:     Serial.println("Ready"); break;
    case eBlocked:   Serial.println("Blocked"); break;
    case eSuspended: Serial.println("Suspended"); break;
    case eDeleted:   Serial.println("Deleted"); break;
    default:         Serial.println("Unknown"); break;
  }
}

TaskHandle_t task1, task2;

void loop() {
  printTaskState(task1, "Task1");
  printTaskState(task2, "Task2");
  Serial.println();
  
  vTaskDelay(pdMS_TO_TICKS(2000));
}
```

## Stack Overflow Detection

Enable in `sdkconfig` or Arduino IDE:
```
CONFIG_FREERTOS_CHECK_STACKOVERFLOW=2
```

```cpp
// Hook called when stack overflow detected
extern "C" void vApplicationStackOverflowHook(TaskHandle_t xTask, char* pcTaskName) {
  Serial.print("STACK OVERFLOW in task: ");
  Serial.println(pcTaskName);
  
  // Infinite loop to halt system
  while(1);
}
```

## Idle Hook (Background Tasks)

```cpp
// Called during idle task execution
extern "C" void vApplicationIdleHook() {
  // Keep this FAST (<10ms)
  // Can be used for power management or cleanup
  
  static unsigned long lastPrint = 0;
  if (millis() - lastPrint > 5000) {
    Serial.print("Heap free: ");
    Serial.println(ESP.getFreeHeap());
    lastPrint = millis();
  }
}
```

## Task Statistics

```cpp
void printTaskStats() {
  char buffer[512];
  vTaskList(buffer);
  
  Serial.println("=== Task List ===");
  Serial.println("Name          State  Prio  Stack  Num");
  Serial.println(buffer);
}

void printRunTimeStats() {
  char buffer[512];
  vTaskGetRunTimeStats(buffer);
  
  Serial.println("=== Runtime Stats ===");
  Serial.println("Task            Time            %");
  Serial.println(buffer);
}

void loop() {
  printTaskStats();
  printRunTimeStats();
  
  vTaskDelay(pdMS_TO_TICKS(10000));
}
```

## Priority Guidelines

| Priority | Use Case | Example |
|----------|----------|---------|
| 0 | Idle task (reserved) | System cleanup |
| 1-2 | Background tasks | Logging, LED blink |
| 3-4 | Standard tasks | Sensor reading, display |
| 5-10 | Important tasks | Network, user input |
| 11-24 | Critical/system | WiFi stack, safety |

## Stack Sizing Guide

**Minimum safe sizes:**
- Simple task (LED blink): 1024 bytes
- Serial I/O: 2048 bytes
- WiFi/network: 4096 bytes
- Large buffers/JSON: 8192 bytes

**Formula:**
```
Stack = LocalVars + CallChain + Margin
```

**Example:**
```cpp
void taskExample(void* parameter) {
  char buffer[512];       // 512 bytes
  // Call chain: ~512 bytes
  // Margin: 1024 bytes
  // Total: 2048 bytes minimum
}

xTaskCreate(taskExample, "Ex", 2048, NULL, 1, NULL);
```

## Verification Checklist

- [ ] Task creation return value checked (pdPASS)
- [ ] Stack size validated with uxTaskGetStackHighWaterMark()
- [ ] Priority in valid range (0-24)
- [ ] Task function never returns (use while(true) or vTaskDelete)
- [ ] Core affinity set correctly (0 or 1) on ESP32
- [ ] Task handle stored if suspension/deletion needed
- [ ] Stack overflow detection enabled in config
