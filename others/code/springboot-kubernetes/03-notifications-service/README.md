# User Management Microservice

## X-Ray Enablement
### Change-1: pom.xml
```xml
		<!--  AWS X-Ray -->			
		<dependency>
    		<groupId>com.amazonaws</groupId>
    		<artifactId>aws-xray-recorder-sdk-spring</artifactId>
    		<version>2.6.1</version>
		</dependency>
```

### Change-2: AwsXrayConfig.java
```java
package com.stacksimplify.restservices.xray;
import javax.servlet.Filter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import com.amazonaws.xray.javax.servlet.AWSXRayServletFilter;

@Configuration
public class AwsXrayConfig {
	@Bean
	public Filter TracingFilter() {
		return new AWSXRayServletFilter("usermanagement-microservice");
	}

}

```

### Change-3: XRayInspector.java
```java
import java.util.Map;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.stereotype.Component;

import com.amazonaws.xray.entities.Subsegment;
import com.amazonaws.xray.spring.aop.AbstractXRayInterceptor;
@Aspect
@Component
public class XRayInspector extends AbstractXRayInterceptor  {

	@Override
	protected Map<String, Map<String, Object>> generateMetadata(ProceedingJoinPoint proceedingJoinPoint,
			Subsegment subsegment) {
		return super.generateMetadata(proceedingJoinPoint, subsegment);
	}

	@Override
	@Pointcut("@within(com.amazonaws.xray.spring.aop.XRayEnabled) && bean(*)")
	public void xrayEnabledClasses() {
	}

}

```

### Change-4: Update @XRayEnabled in Controllers
```java
@RestController
@XRayEnabled
public class NotificationController {
}
```
