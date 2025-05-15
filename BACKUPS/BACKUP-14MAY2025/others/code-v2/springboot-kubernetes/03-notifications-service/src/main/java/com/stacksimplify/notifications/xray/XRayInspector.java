package com.stacksimplify.notifications.xray;

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
