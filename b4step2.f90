! ============================================
subroutine b4step2(mbc,mx,my,meqn,q,xlower,ylower,dx,dy,t,dt,maux,aux)
! ============================================
!
! # called before each call to step
! # use to set time-dependent aux arrays or perform other tasks.
!
! This particular routine sets negative values of q(1,i,j) to zero,
! as well as the corresponding q(m,i,j) for m=1,meqn.
! This is for problems where q(1,i,j) is a depth.
! This should occur only because of rounding error.
!
! Also calls movetopo if topography might be moving.

    use geoclaw_module, only: dry_tolerance
    use geoclaw_module, only: g => grav
    use topo_module, only: num_dtopo,topotime
    use topo_module, only: aux_finalized
    use topo_module, only: xlowdtopo,xhidtopo,ylowdtopo,yhidtopo

    use amr_module, only: xlowdomain => xlower
    use amr_module, only: ylowdomain => ylower
    use amr_module, only: xhidomain => xupper
    use amr_module, only: yhidomain => yupper
    use amr_module, only: xperdom,yperdom,spheredom,NEEDS_TO_BE_SET
	
    use storm_module, only: set_storm_fields
	!use barrier_breach
    implicit none

    ! Subroutine arguments
    integer, intent(in) :: meqn
    integer, intent(inout) :: mbc,mx,my,maux
    real(kind=8), intent(inout) :: xlower, ylower, dx, dy, t, dt
    real(kind=8), intent(inout) :: q(meqn,1-mbc:mx+mbc,1-mbc:my+mbc)
    real(kind=8), intent(inout) :: aux(maux,1-mbc:mx+mbc,1-mbc:my+mbc)
	

    ! Local storage
    integer :: index,i,j,k,dummy
    real(kind=8) :: h,u,v
	
    ! Check for NaNs in the solution
    call check4nans(meqn,mbc,mx,my,q,t,1)

    ! check for h < 0 and reset to zero
    ! check for h < drytolerance
    ! set hu = hv = 0 in all these cells
    forall(i=1-mbc:mx+mbc, j=1-mbc:my+mbc,q(1,i,j) < dry_tolerance)
        q(1,i,j) = max(q(1,i,j),0.d0)
        q(2:3,i,j) = 0.d0
    end forall
	

    if (aux_finalized < 2) then
        print *, 'RESETTING AUX'
        ! topo arrays might have been updated by dtopo more recently than
        ! aux arrays were set unless at least 1 step taken on all levels
        aux(1,:,:) = NEEDS_TO_BE_SET ! new system checks this val before setting
        call setaux(mbc,mx,my,xlower,ylower,dx,dy,maux,aux)
    endif

    ! !!!!!Change xlower and ylower compare values to varialbes read from file 
   if ((xlower > -88.0) .and. (xlower < -86.0) .and. &
        (ylower < 25.7) .and. (ylower > 25.5)) then
       
           print *, 'Gonna call barrier breach!'
           call barrier_breach(maux,mbc,mx,my,xlower,ylower,dx,dy,t,dt,aux)
       
   end if
   
    ! Set wind and pressure aux variables for this grid
    call set_storm_fields(maux,mbc,mx,my,xlower,ylower,dx,dy,t,aux)

end subroutine b4step2

subroutine barrier_breach(maux,mbc,mx,my,xlower,ylower,dx,dy,t,dt,aux)
implicit none

! Allocate variables
! Subroutine variables
integer, intent(inout) :: mbc,mx,my,maux
real(kind=8), intent(inout) :: xlower, ylower, dx, dy, t, dt
real(kind=8), intent(inout) :: aux(maux,1-mbc:mx+mbc,1-mbc:my+mbc)

! Local variables
! integer, parameter :: dp = selected_real_kind(15, 307)
real, allocatable, dimension(:) ::  row
integer :: i, j,  t1, t2, rowidx, colidx
real ::  amp_max, sigma, h0, x1, x2, col, stepx, stepy, dtime, amp
real :: time(10) != (/(i, i=0,9, 1)/)
!real, dimension(10) :: amp
integer, dimension(10) :: zero_array
integer, dimension(10) :: one_array
real, dimension(600) :: y 
real,allocatable, dimension(:,:) :: X_mesh, Y_mesh, breach
real, dimension(500) :: x 
CHARACTER(*), PARAMETER :: fileplace = "/home/cat/claw/clawpack-v5.5.0/geoclaw/scratch/"

! do j=1-mbc,my+mbc
    !     y = ylower + (j-0.5d0) * dy
    !     do i=1-mbc,mx+mbc
    !         x = xlower + (i-0.5d0) * dx
    !         ! Location logic
    !         aux(1, i, j) = something
    !     end do
    ! end do

! Determine number of increments for X_mesh and Y_mesh
! stepx = (100.0 + 100.0)/ 499.0
! stepy = (60e3 / 599)

! fill x and y like np.linspace
! x = (/((i-1)*stepx -100.0, i=1,500)/)
! y = (/((i-1)* stepy + 0, i=1, 600)/)

do j=1-mbc,my+mbc
        y = ylower + (j-0.5d0) * dy
        do i=1-mbc,mx+mbc
            x = xlower + (i-0.5d0) * dx
            print *, size(x), size(y)
        end do
    end do

t1 = -200000.0
t2 = 6.0
amp_max = 5.0
dtime = 10.0/9.0 !!!!! what is this doing!
time(1:10) = [(0 + ((i-1)*dtime),i=1, 10)]

zero_array = 0
one_array = 1

!do i = 1, 10
!	if (time(i) < t1) then
!		amp(i) = zero_array(i)
!	elseif (t1 <= time(i) .and. time(i) < t2) then
!		amp(i) =  (amp_max / (t2 - t1) * (time(i) - t1))
!	elseif (t2 <= time(i)) then
!		amp(i) = one_array(i) * amp_max
!end if
!
!end do

! fill x and y matrices a la np.meshgrid
allocate(X_mesh(size(y), size(x)))
allocate(Y_mesh(size(y), size(x)))
do i=1, size(y)
    do j=1, size(x)
        X_mesh(i,j) = x(j)
        Y_mesh(i,j) = y(i)
    end do
end do
! Add breach parameters
!!!!!! change these to imported from b4step2 subroutine
x1 = -86.0
x2 = -88.0
sigma = 10.0
h0 = 10.0
allocate(breach(size(X_mesh, 1), size(X_mesh, 2)))
! Initialize breach to match initial height
!do i= 1, size(X_mesh,2)
!	breach(:,i) = h0
!	do j = 1, size(X_mesh,1)
!		breach(j,:) = h0
!	end do
!end do
breach(:,:) = aux(1, :, :)
! Breach the barrier island depending on time
if (t<t1) then
    amp =0.0
elseif (t>t1) then
    amp=10.0
end if

!do i = 1, size(amp)
	do rowidx = 1, size(X_mesh, 1)
		row = X_mesh(rowidx,:)
			do colidx = 1, size(X_mesh, 2)
				col = X_mesh(rowidx, colidx)
				if (col >= x1 .and. col <= x2) then
					breach(rowidx, colidx) = breach(rowidx, colidx) &
					- (amp * exp(-X_mesh(rowidx, colidx)**2/(sigma**2)) &
					* 0.1 * Y_mesh(rowidx, colidx))
				end if
			end do
	end do
!end do

aux(1,:,:) = breach(:,:)
print *, maxval(breach)
! do j=1-mbc,my+mbc
    !     y = ylower + (j-0.5d0) * dy
    !     do i=1-mbc,mx+mbc
    !         x = xlower + (i-0.5d0) * dx
    !         ! Location logic
    !         aux(1, i, j) = something
    !     end do
    ! end do

end subroutine barrier_breach