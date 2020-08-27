package com.stacksimplify.notifications.core.services;

import com.stacksimplify.notifications.core.dtos.EmailMessage;

public interface NotificationService {

	public void sendEmail(EmailMessage emailMessage);

}
