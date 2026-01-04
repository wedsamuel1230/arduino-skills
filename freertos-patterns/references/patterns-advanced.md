# Advanced FreeRTOS Patterns

## Task Notifications (Lightweight Alternative to Semaphores)

```cpp
TaskHandle_t workerTaskHandle;

void taskWorker(void* parameter) {
  uint32_t notificationValue;
  
  while(true) {
    // Wait for notification (clears counter on read)
    notificationValue = ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
    
    Serial.printf("Received %lu notifications\n", notificationValue);
    
    // Process work
    for (uint32_t i = 0; i < notificationValue; i++) {
      Serial.printf("Processing task %lu...\n", i + 1);
      vTaskDelay(pdMS_TO_TICKS(100));
    }
  }
}

void taskController(void* parameter) {
  uint32_t workCount = 1;
  
  while(true) {
    vTaskDelay(pdMS_TO_TICKS(2000));
    
    Serial.printf("Sending %lu work items\n", workCount);
    
    // Notify worker (increment notification count)
    xTaskNotifyGive(workerTaskHandle);
    
    workCount = (workCount % 5) + 1;
  }
}

void setup() {
  Serial.begin(115200);
  
  xTaskCreate(taskWorker, "Worker", 2048, NULL, 2, &workerTaskHandle);
  xTaskCreate(taskController, "Controller", 2048, NULL, 1, NULL);
}
```

## Event Groups (Complex Synchronization)

```cpp
EventGroupHandle_t systemEvents;

// Event bits
#define BIT_WIFI_CONNECTED    (1 << 0)
#define BIT_SENSOR_READY      (1 << 1)
#define BIT_SD_MOUNTED        (1 << 2)
#define BIT_ALL_READY         (BIT_WIFI_CONNECTED | BIT_SENSOR_READY | BIT_SD_MOUNTED)

void taskInitWiFi(void* parameter) {
  Serial.println("Initializing WiFi...");
  vTaskDelay(pdMS_TO_TICKS(2000));
  
  Serial.println("WiFi connected");
  xEventGroupSetBits(systemEvents, BIT_WIFI_CONNECTED);
  
  vTaskDelete(NULL);
}

void taskInitSensor(void* parameter) {
  Serial.println("Initializing sensor...");
  vTaskDelay(pdMS_TO_TICKS(1500));
  
  Serial.println("Sensor ready");
  xEventGroupSetBits(systemEvents, BIT_SENSOR_READY);
  
  vTaskDelete(NULL);
}

void taskInitSD(void* parameter) {
  Serial.println("Mounting SD card...");
  vTaskDelay(pdMS_TO_TICKS(1000));
  
  Serial.println("SD mounted");
  xEventGroupSetBits(systemEvents, BIT_SD_MOUNTED);
  
  vTaskDelete(NULL);
}

void taskStartup(void* parameter) {
  Serial.println("Waiting for all subsystems...");
  
  // Wait for all bits (AND logic)
  EventBits_t bits = xEventGroupWaitBits(
    systemEvents,
    BIT_ALL_READY,
    pdFALSE,  // Don't clear bits
    pdTRUE,   // Wait for ALL bits
    portMAX_DELAY
  );
  
  if ((bits & BIT_ALL_READY) == BIT_ALL_READY) {
    Serial.println("All subsystems ready!");
    Serial.println("Starting main application...");
  }
  
  vTaskDelete(NULL);
}

void setup() {
  Serial.begin(115200);
  
  systemEvents = xEventGroupCreate();
  
  xTaskCreate(taskInitWiFi, "InitWiFi", 4096, NULL, 1, NULL);
  xTaskCreate(taskInitSensor, "InitSensor", 2048, NULL, 1, NULL);
  xTaskCreate(taskInitSD, "InitSD", 2048, NULL, 1, NULL);
  xTaskCreate(taskStartup, "Startup", 2048, NULL, 2, NULL);
}
```

## Software Timers

```cpp
TimerHandle_t periodicTimer;
TimerHandle_t oneShotTimer;
uint32_t timerCount = 0;

void periodicCallback(TimerHandle_t xTimer) {
  timerCount++;
  Serial.printf("Periodic timer: %lu\n", timerCount);
  
  // Keep this FAST (<10ms)
}

void oneShotCallback(TimerHandle_t xTimer) {
  Serial.println("One-shot timer fired!");
}

void setup() {
  Serial.begin(115200);
  
  // Create periodic timer (1 second, auto-reload)
  periodicTimer = xTimerCreate(
    "Periodic",
    pdMS_TO_TICKS(1000),
    pdTRUE,  // Auto-reload
    NULL,
    periodicCallback
  );
  
  // Create one-shot timer (5 seconds, no auto-reload)
  oneShotTimer = xTimerCreate(
    "OneShot",
    pdMS_TO_TICKS(5000),
    pdFALSE,  // One-shot
    NULL,
    oneShotCallback
  );
  
  // Start timers
  if (periodicTimer != NULL) {
    xTimerStart(periodicTimer, 0);
  }
  
  if (oneShotTimer != NULL) {
    xTimerStart(oneShotTimer, 0);
  }
}

void loop() {
  vTaskDelay(portMAX_DELAY);
}
```

## Watchdog Integration

```cpp
#include <esp_task_wdt.h>

#define WDT_TIMEOUT 3  // 3 seconds

void taskCritical(void* parameter) {
  // Register with watchdog
  esp_task_wdt_add(NULL);
  
  while(true) {
    // Critical operations
    readSafetySensors();
    updateMotorControl();
    
    // Reset watchdog (must happen every 3 seconds)
    esp_task_wdt_reset();
    
    vTaskDelay(pdMS_TO_TICKS(100));
  }
}

void taskNonCritical(void* parameter) {
  while(true) {
    // Non-critical work (no watchdog)
    updateDisplay();
    logData();
    
    vTaskDelay(pdMS_TO_TICKS(500));
  }
}

void setup() {
  Serial.begin(115200);
  
  // Initialize watchdog
  esp_task_wdt_init(WDT_TIMEOUT, true);  // Panic on timeout
  
  xTaskCreate(taskCritical, "Critical", 4096, NULL, 10, NULL);
  xTaskCreate(taskNonCritical, "NonCritical", 4096, NULL, 1, NULL);
  
  Serial.println("Watchdog enabled");
}
```

## Stream Buffers (High-Throughput Data)

```cpp
StreamBufferHandle_t uartStream;

void taskUARTReceiver(void* parameter) {
  uint8_t buffer[128];
  
  while(true) {
    if (Serial.available()) {
      int bytesRead = Serial.readBytes(buffer, sizeof(buffer));
      
      // Send to stream buffer
      size_t bytesSent = xStreamBufferSend(
        uartStream,
        buffer,
        bytesRead,
        pdMS_TO_TICKS(100)
      );
      
      if (bytesSent < bytesRead) {
        Serial.println("Stream buffer full, data lost!");
      }
    }
    
    vTaskDelay(pdMS_TO_TICKS(10));
  }
}

void taskDataProcessor(void* parameter) {
  uint8_t buffer[128];
  
  while(true) {
    // Wait for at least 1 byte
    size_t bytesReceived = xStreamBufferReceive(
      uartStream,
      buffer,
      sizeof(buffer),
      portMAX_DELAY
    );
    
    if (bytesReceived > 0) {
      Serial.printf("Processing %d bytes\n", bytesReceived);
      // Process data...
    }
  }
}

void setup() {
  Serial.begin(115200);
  
  // Create stream buffer (1024 bytes)
  uartStream = xStreamBufferCreate(1024, 1);  // Trigger level = 1 byte
  
  xTaskCreate(taskUARTReceiver, "UART_RX", 2048, NULL, 2, NULL);
  xTaskCreate(taskDataProcessor, "Processor", 4096, NULL, 1, NULL);
}
```

## Task Notifications with Value

```cpp
TaskHandle_t controlTaskHandle;

enum ControlCommand {
  CMD_START = 1,
  CMD_STOP = 2,
  CMD_RESET = 3,
  CMD_STATUS = 4
};

void taskControl(void* parameter) {
  uint32_t command;
  
  while(true) {
    // Wait for notification with value
    if (xTaskNotifyWait(0, 0xFFFFFFFF, &command, portMAX_DELAY) == pdPASS) {
      switch(command) {
        case CMD_START:
          Serial.println("Starting...");
          break;
          
        case CMD_STOP:
          Serial.println("Stopping...");
          break;
          
        case CMD_RESET:
          Serial.println("Resetting...");
          break;
          
        case CMD_STATUS:
          Serial.println("Status: Running");
          break;
          
        default:
          Serial.println("Unknown command");
          break;
      }
    }
  }
}

void taskCommandSender(void* parameter) {
  ControlCommand commands[] = {CMD_START, CMD_STATUS, CMD_STOP, CMD_RESET};
  int cmdIndex = 0;
  
  while(true) {
    vTaskDelay(pdMS_TO_TICKS(2000));
    
    // Send command via task notification
    xTaskNotify(controlTaskHandle, commands[cmdIndex], eSetValueWithOverwrite);
    
    cmdIndex = (cmdIndex + 1) % 4;
  }
}

void setup() {
  Serial.begin(115200);
  
  xTaskCreate(taskControl, "Control", 2048, NULL, 2, &controlTaskHandle);
  xTaskCreate(taskCommandSender, "Sender", 2048, NULL, 1, NULL);
}
```

## Direct-to-Task Notifications from ISR

```cpp
#define BUTTON_PIN 0

TaskHandle_t buttonTaskHandle;
volatile uint32_t isrCount = 0;

void IRAM_ATTR buttonISR() {
  BaseType_t xHigherPriorityTaskWoken = pdFALSE;
  
  // Notify task from ISR
  vTaskNotifyGiveFromISR(buttonTaskHandle, &xHigherPriorityTaskWoken);
  
  isrCount++;
  
  if (xHigherPriorityTaskWoken) {
    portYIELD_FROM_ISR();
  }
}

void taskButtonHandler(void* parameter) {
  uint32_t notificationCount;
  
  while(true) {
    // Wait for ISR notification
    notificationCount = ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
    
    Serial.printf("Button events: %lu (ISR count: %lu)\n", 
                  notificationCount, isrCount);
    
    // Debounce
    vTaskDelay(pdMS_TO_TICKS(200));
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  xTaskCreate(taskButtonHandler, "Button", 2048, NULL, 3, &buttonTaskHandle);
  
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonISR, FALLING);
}
```

## Task Suspend/Resume Pattern

```cpp
TaskHandle_t workerTaskHandle;

void taskWorker(void* parameter) {
  while(true) {
    Serial.println("Worker: Doing work...");
    vTaskDelay(pdMS_TO_TICKS(500));
  }
}

void taskSupervisor(void* parameter) {
  bool workerSuspended = false;
  
  while(true) {
    vTaskDelay(pdMS_TO_TICKS(3000));
    
    if (workerSuspended) {
      Serial.println("Supervisor: Resuming worker");
      vTaskResume(workerTaskHandle);
    } else {
      Serial.println("Supervisor: Suspending worker");
      vTaskSuspend(workerTaskHandle);
    }
    
    workerSuspended = !workerSuspended;
  }
}

void setup() {
  Serial.begin(115200);
  
  xTaskCreate(taskWorker, "Worker", 2048, NULL, 1, &workerTaskHandle);
  xTaskCreate(taskSupervisor, "Supervisor", 2048, NULL, 2, NULL);
}
```

## Dual-Core Task Pinning

```cpp
void taskCore0(void* parameter) {
  while(true) {
    // WiFi/BLE operations (protocol stack on Core 0)
    Serial.printf("Core 0: %d\n", xPortGetCoreID());
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void taskCore1(void* parameter) {
  while(true) {
    // Application logic (Core 1)
    Serial.printf("Core 1: %d\n", xPortGetCoreID());
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void setup() {
  Serial.begin(115200);
  
  // Pin tasks to specific cores
  xTaskCreatePinnedToCore(taskCore0, "Core0", 4096, NULL, 2, NULL, 0);
  xTaskCreatePinnedToCore(taskCore1, "Core1", 4096, NULL, 1, NULL, 1);
}
```

## Task List Debugging

```cpp
void printTaskList() {
  char buffer[512];
  vTaskList(buffer);
  
  Serial.println("\n=== Task List ===");
  Serial.println("Name          State  Prio  Stack  Num");
  Serial.println("-------------------------------------");
  Serial.println(buffer);
}

void printRunTimeStats() {
  char buffer[512];
  vTaskGetRunTimeStats(buffer);
  
  Serial.println("\n=== Runtime Stats ===");
  Serial.println("Task            Time            %");
  Serial.println("------------------------------------");
  Serial.println(buffer);
}

void loop() {
  printTaskList();
  printRunTimeStats();
  
  vTaskDelay(pdMS_TO_TICKS(10000));
}
```

## Idle Task Hook

```cpp
extern "C" void vApplicationIdleHook() {
  // Called during idle task execution
  // Keep this VERY FAST (<100µs)
  
  static unsigned long lastCheck = 0;
  unsigned long now = millis();
  
  if (now - lastCheck > 10000) {
    // Periodic maintenance (every 10 seconds)
    lastCheck = now;
  }
}
```

## Tick Hook (Periodic Callback)

```cpp
extern "C" void vApplicationTickHook() {
  // Called every tick (default: 1ms)
  // Keep this EXTREMELY FAST (<10µs)
  
  static uint32_t tickCount = 0;
  tickCount++;
  
  // Example: Toggle GPIO every 1000 ticks (1 second)
  if (tickCount % 1000 == 0) {
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  }
}
```

## Best Practices

1. **Prefer task notifications** - Faster than semaphores (45% less overhead)
2. **Use event groups for complex sync** - Multiple condition wait
3. **Stream buffers for data pipes** - High-throughput, low-latency
4. **Software timers for periodic tasks** - If no blocking operations
5. **Watchdog for critical tasks** - Safety-critical systems
6. **Suspend/resume sparingly** - Can cause priority inversion
7. **Core pinning for performance** - Separate protocol stack from app logic

## Performance Comparison

| Mechanism | RAM Overhead | Wake Latency | Throughput |
|-----------|--------------|--------------|------------|
| Task Notification | 8 bytes | ~3µs | High |
| Binary Semaphore | 80 bytes | ~5µs | Medium |
| Queue | 80 + (N×itemSize) | ~7µs | Medium |
| Stream Buffer | bufferSize + 80 | ~4µs | Very High |
| Event Groups | 24 bytes | ~6µs | Low |

## Verification Checklist

- [ ] Task notifications used instead of semaphores where possible
- [ ] Event groups only for complex synchronization
- [ ] Software timers callback duration <10ms
- [ ] Watchdog timeout appropriate (3-10 seconds)
- [ ] Stream buffers sized for peak throughput
- [ ] Idle hook duration <100µs
- [ ] Tick hook duration <10µs (or disabled)
- [ ] Core affinity set correctly (0 for WiFi, 1 for app)
