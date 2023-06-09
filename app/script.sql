USE [CHECKIN]
GO
/****** Object:  Table [dbo].[Accounts]    Script Date: 5/12/2023 10:08:48 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Accounts](
	[ID] [char](36) NOT NULL,
	[UserName] [varchar](100) NULL,
	[Password] [varchar](50) NULL,
	[Address] [nvarchar](500) NULL,
	[FirstName] [nvarchar](100) NULL,
	[LastName] [nvarchar](100) NULL,
	[Email] [varchar](100) NULL,
	[Phone] [varchar](50) NULL,
	[CustomerID] [char](36) NULL,
	[CreatedDate] [datetime] NULL,
 CONSTRAINT [PK_Account] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Customers]    Script Date: 5/12/2023 10:08:48 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Customers](
	[ID] [char](36) NOT NULL,
	[CustomerName] [nvarchar](500) NULL,
	[Address] [nvarchar](500) NULL,
	[Phone] [char](20) NULL,
	[Email] [varchar](100) NULL,
	[MasterUserName] [varchar](225) NULL,
	[MasterPassword] [varchar](50) NULL,
	[CreatedDate] [datetime] NULL,
 CONSTRAINT [PK_Customers] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[faces]    Script Date: 5/12/2023 10:08:48 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[faces](
	[ID] [char](36) NOT NULL,
	[_id] [varchar](512) NULL,
	[_index] [varchar](100) NULL,
	[Extension] [varchar](10) NULL,
	[AccountID] [char](36) NULL,
	[Type] [int] NULL,
 CONSTRAINT [PK_faces] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Accounts]  WITH CHECK ADD  CONSTRAINT [FK_Accounts_Customers] FOREIGN KEY([CustomerID])
REFERENCES [dbo].[Customers] ([ID])
GO
ALTER TABLE [dbo].[Accounts] CHECK CONSTRAINT [FK_Accounts_Customers]
GO
ALTER TABLE [dbo].[faces]  WITH CHECK ADD  CONSTRAINT [FK_faces_Accounts] FOREIGN KEY([AccountID])
REFERENCES [dbo].[Accounts] ([ID])
GO
ALTER TABLE [dbo].[faces] CHECK CONSTRAINT [FK_faces_Accounts]
GO
