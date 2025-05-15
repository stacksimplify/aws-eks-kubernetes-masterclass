package com.stacksimplify.restservices.xray;
import java.net.URL;

import javax.servlet.Filter;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.amazonaws.xray.AWSXRay;
import com.amazonaws.xray.AWSXRayRecorderBuilder;
import com.amazonaws.xray.javax.servlet.AWSXRayServletFilter;
import com.amazonaws.xray.plugins.EC2Plugin;
import com.amazonaws.xray.plugins.EKSPlugin;
import com.amazonaws.xray.plugins.ElasticBeanstalkPlugin;
import com.amazonaws.xray.strategy.sampling.LocalizedSamplingStrategy;

@Configuration
public class AwsXrayConfig {
	@Bean
	public Filter TracingFilter() {
		return new AWSXRayServletFilter("usermanagement-microservice");
	}

	  static {
		    AWSXRayRecorderBuilder builder = AWSXRayRecorderBuilder.standard()
		    		.withPlugin(new EC2Plugin())
		    		.withPlugin(new ElasticBeanstalkPlugin())
		    		.withPlugin(new EKSPlugin());

		    URL ruleFile = AwsXrayConfig.class.getResource("/sampling-rules.json");
		    builder.withSamplingStrategy(new LocalizedSamplingStrategy(ruleFile));

		    AWSXRay.setGlobalRecorder(builder.build());
		  }
	
}
